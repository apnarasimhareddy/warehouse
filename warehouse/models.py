from warehouse.core.db import Base
from sqlalchemy import Column,Integer,String,DateTime, Enum as SQLEnum,Date
from sqlalchemy.sql import func
from warehouse.enums import CampaignsStatus,CustomerStatus


class Customers(Base):

    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True,index=True)
    name = Column(String(80), nullable=False)
    email = Column(String(128),index=True,unique=True)
    status = Column(SQLEnum(CustomerStatus),nullable=False)
    createdTime = Column(DateTime,default=func.now(),nullable=False,server_default=func.now())
    

class Campaigns(Base):

    __tablename__ = 'campaigns'

    id = Column(Integer, primary_key=True,index=True)
    name = Column(String(80), nullable=False)
    budget = Column(Integer,nullable=False)
    status = Column(SQLEnum(CampaignsStatus),nullable=False)
    startDate = Column(Date,nullable=False)
    endDate = Column(Date,nullable=False)
