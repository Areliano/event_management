from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app.core.database import get_db
from app.core.auth import get_current_user, get_current_organizer
from app.models.event import Event
from app.schemas.event import EventCreate, EventOut

router = APIRouter(prefix="/events", tags=["Events"])

@router.post("/", response_model=EventOut)
def create_event(
    event: EventCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_organizer)
):
    new_event = Event(**event.dict(), organizer_id=current_user.id)
    db.add(new_event)
    db.commit()
    db.refresh(new_event)
    return new_event

@router.get("/", response_model=List[EventOut])
def list_events(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 10,
    date: Optional[datetime] = None,
    location: Optional[str] = None,
    keyword: Optional[str] = None
):
    query = db.query(Event)
    if date:
        query = query.filter(Event.date == date)
    if location:
        query = query.filter(Event.location.ilike(f"%{location}%"))
    if keyword:
        query = query.filter(Event.title.ilike(f"%{keyword}%"))
    return query.offset(skip).limit(limit).all()
