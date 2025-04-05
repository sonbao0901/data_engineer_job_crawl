from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TopcvDataJobBase(BaseModel):
    title: str
    company: str
    logo: Optional[str] = None
    url: Optional[str] = None
    location: Optional[str] = None
    salary: Optional[str] = None

class TopcvDataJobCreate(TopcvDataJobBase):
    pass

class TopcvDataJob(TopcvDataJobBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class ItviecDataJobBase(BaseModel):
    title: str
    company: str
    logo: Optional[str] = None
    url: Optional[str] = None
    location: Optional[str] = None
    mode: Optional[str] = None
    tags: Optional[str] = None
    descriptions: Optional[str] = None
    requirements: Optional[str] = None

class ItviecDataJobCreate(ItviecDataJobBase):
    pass

class ItviecDataJob(ItviecDataJobBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True