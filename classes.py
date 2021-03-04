from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Device(Base):
  __tablename__ = 'device'
  id = Column(Integer, primary_key=True)
  address = Column(String(48), index=True)
  name = Column(String(48))
  uom = Column(String(1))

Index('address', Device.address, unique=True)

class Probe(Base):
  __tablename__ = 'probe'
  id = Column(Integer, primary_key=True)
  device_id = Column(Integer, ForeignKey(Device.id))
  probe_number = Column(Integer)
  name = Column(String(48))

Index('device_id/probe_number', Probe.device_id, Probe.probe_number, unique=True)

class Temp(Base):
  __tablename__ = 'temps'
  id = Column(Integer, primary_key=True)
  poll_date = Column(DateTime, index=True)
  device_id = Column(Integer, ForeignKey(Device.id))
  probe_id = Column(Integer, ForeignKey(Probe.id))
  temp = Column(Integer)
  uom = Column(String(1))
  device = relationship("Device")
  probe = relationship("Probe")

Index('poll_date/device_id/probe', Temp.poll_date, Temp.device_id, Temp.probe_id, unique=True)
