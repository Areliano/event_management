# app/schemas/rsvp.py
from pydantic import BaseModel

class RSVPCreate(BaseModel):
    event_id: int

class RSVPOut(BaseModel):
    id: int
    user_id: int
    event_id: int
    approved: bool

    class Config:
        orm_mode = True
