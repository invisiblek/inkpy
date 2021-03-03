from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Temp(Base):
  __tablename__ = 'temps'
  id = Column(Integer, primary_key=True)
  poll_date = Column(DateTime, index=True)
  device = Column(String(48), index=True)
  probe = Column(Integer, index=True)
  temp = Column(Integer)

Index('poll_date/device/probe', Temp.poll_date, Temp.device, Temp.probe, unique=True)
