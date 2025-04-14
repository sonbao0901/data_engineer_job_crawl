from sqlalchemy import Column, Integer, String, Text, DateTime, func
from database import Base

class TopcvDataJob(Base):
    __tablename__ = 'topcv_data_job'
    __table_args__ = {'schema': 'bronze'}
    
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    company = Column(String(150), nullable=False)
    logo = Column(Text)
    url = Column(Text, unique=True)
    location = Column(String(100))
    salary = Column(String(50))
    requirements = Column(Text)
    descriptions = Column(Text)
    experience = Column(String(50))
    education = Column(String(100))
    type_of_work = Column(String(50))
    created_at = Column(DateTime, default=func.current_timestamp())

class ItviecDataJob(Base):
    __tablename__ = 'itviec_data_job'
    __table_args__ = {'schema': 'bronze'}
    
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    company = Column(String(150), nullable=False)
    logo = Column(Text)
    url = Column(Text, unique=True)
    location = Column(String(100))
    mode = Column(String(50))
    tags = Column(String(200))
    descriptions = Column(Text)
    requirements = Column(Text)
    created_at = Column(DateTime, default=func.current_timestamp())