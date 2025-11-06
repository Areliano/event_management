# app/models/event.py
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    location = Column(String(200))
    date = Column(DateTime, nullable=False)
    max_attendees = Column(Integer, nullable=False, default=50)
    organizer_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    organizer = relationship("User", backref="events")
    rsvps = relationship("app.models.rsvp.RSVP", back_populates="event", cascade="all, delete-orphan")
