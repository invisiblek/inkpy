#!/usr/bin/env python3

from classes import *
from configparser import ConfigParser
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker

import sys

config = ConfigParser()
config.read("app.cfg")

if config['APP']['db_type'] == "sqlite":
  sql_uri = "sqlite:///{}".format(config['APP']['db_filename'])
elif config['APP']['db_type'] == "mysql":
  sql_uri = "mysql://{}:{}@{}:{}/{}".format(config['APP']['db_user'], config['APP']['db_pass'], config['APP']['db_host'], config['APP']['db_port'], config['APP']['db_name'])

engine = create_engine(sql_uri)

if not database_exists(engine.url):
  print("database doesn't exist, bailing")
  sys.exit

engine.connect()
Session = sessionmaker(bind=engine)
session = Session()

cutoff_time = datetime.now() - timedelta(hours=int(config['APP']['max_data_storage']))
session.query(Temp).filter(Temp.poll_date < cutoff_time).delete()
session.commit()
