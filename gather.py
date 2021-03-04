#!/usr/bin/env python3

from array import array
from bluepy import btle
from classes import *
from constants import *
from configparser import ConfigParser
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker

import time
import struct
import sys

debug = False

next_storage_time = datetime.now()

client = None
service = None
characteristics = None

config = ConfigParser()
config.read("app.cfg")

if config['APP']['db_type'] == "sqlite":
  sql_uri = "sqlite:///{}".format(config['APP']['db_filename'])
elif config['APP']['db_type'] == "mysql":
  sql_uri = "mysql://{}:{}@{}:{}/{}".format(config['APP']['db_user'], config['APP']['db_pass'], config['APP']['db_host'], config['APP']['db_port'], config['APP']['db_name'])

engine = create_engine(sql_uri)

if not database_exists(engine.url):
  create_database(engine.url)
else:
  engine.connect()

Device.__table__.create(bind=engine, checkfirst=True)
Probe.__table__.create(bind=engine, checkfirst=True)
Temp.__table__.create(bind=engine, checkfirst=True)

Session = sessionmaker(bind=engine)
session = Session()

inkbird = None
query = session.query(Device).filter(Device.address == config['APP']['device'])
if not query.scalar():
  inkbird = Device(address=config['APP']['device'],
             name="inkbird")
  session.add(inkbird)
  session.commit()
else:
  inkbird = query.first()

probes = {}

def getbbqclient():
  global client
  global service
  global characteristics

  client = btle.Peripheral(config['APP']['device'])
  service = client.getServiceByUUID(SERVICE_UUID)
  characteristics = service.getCharacteristics()

  # unknown shit
  client.writeCharacteristic(characteristics[0].getHandle() + 1, b"\x01\x00", withResponse = True)
  client.writeCharacteristic(characteristics[3].getHandle() + 1, b"\x01\x00", withResponse = True)

  # login
  characteristics[1].write(CREDENTIALS_MESSAGE, withResponse = True)

  # enable data
  characteristics[4].write(REALTIME_DATA_ENABLE_MESSAGE, withResponse = True)

  # set fahrenheit
  characteristics[4].write(UNITS_F_MESSAGE, withResponse = True)

def handletemperature(data):
  temps = array("H")
  temps.frombytes(data)

  now = datetime.now()
  for temp in list(enumerate(temps)):
    if temp[0] not in probes:
      query = session.query(Probe).filter(Probe.device_id == inkbird.id, Probe.probe_number == temp[0])
      if not query.scalar():
        p = Probe(device_id=inkbird.id,
                  probe_number=temp[0],
                  name="probe{}".format(temp[0]))
        session.add(p)
        session.commit()
        probes[temp[0]] = p
      else:
        probes[temp[0]] = query.first()

    print("{}: {}: {}".format(config['APP']['device'], temp[0], temp[1]))
    temp = Temp(poll_date=now,
                device_id=inkbird.id,
                probe_id = probes[temp[0]].id,
                temp = temp[1])
    session.add(temp)
    session.commit()

def handlebattery(data):
  if data[0] != 36:
    return
  battery, maxBattery = struct.unpack("<HH", data[1:5])
  battery = int(battery/maxBattery * 100)
  print(battery)

class NotificationDelegate(btle.DefaultDelegate):
  def handleNotification(self, cHandle, data):
    if debug:
      print(cHandle)
      print(data)
      return

    global next_storage_time
    now = datetime.now()
    if now > next_storage_time:
      next_storage_time = now + timedelta(seconds=int(config['APP']['max_storage_rate']))

      if cHandle == 48:
        handletemperature(data)
#      elif cHandle == 37:
#        handlebattery(data)

def gather():
  getbbqclient()
  if not client:
    print("Unable to set up client")
    sys.exit()

  client.setDelegate(NotificationDelegate())

  while True:
    client.waitForNotifications(1.0)

gather()
