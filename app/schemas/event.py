# app/schemas/event.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class EventCreate(BaseModel):
    title: str
    description: Optional[str] = None
    location: Optional[str] = None
    date: datetime
    max_attendees: int

class EventUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    date: Optional[datetime] = None
    max_attendees: Optional[int] = None

class EventOut(BaseModel):
    id: int
    title: str
    description: Optional[str]
    location: Optional[str]
    date: datetime
    max_attendees: int
    organizer_id: int

    class Config:
        orm_mode = True
