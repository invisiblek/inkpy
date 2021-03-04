from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Device(Base):
  __tablename__ = 'device'
  id = Column(Integer, primary_key=True)
  address = Column(String(48), index=True)
  name = Column(String(48))

Index('address', Device.address, unique=True)

class Temp(Base):
  __tablename__ = 'temps'
  id = Column(Integer, primary_key=True)
  poll_date = Column(DateTime, index=True)
  device_id = Column(Integer, ForeignKey(Device.id))
  probe = Column(Integer, index=True)
  temp = Column(Integer)
  device = relationship("Device")

Index('poll_date/device_id/probe', Temp.poll_date, Temp.device_id, Temp.probe, unique=True)
