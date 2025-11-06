from pydantic import BaseModel
from datetime import datetime

class EventCreate(BaseModel):
    title: str
    description: str
    location: str
    date: datetime
    max_attendees: int

class EventOut(EventCreate):
    id: int
    organizer_id: int

    class Config:
        orm_mode = True

class RSVPCreate(BaseModel):
    event_id: int

class RSVPOut(BaseModel):
    id: int
    event_id: int
    user_id: int
    approved: bool

    class Config:
        orm_mode = True
