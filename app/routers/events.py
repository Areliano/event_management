# app/routers/events.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from datetime import date
from app.core.database import get_db
from app.core.auth import get_current_user, get_current_organizer
from app.schemas.event import EventCreate, EventOut, EventUpdate
from app.models.event import Event
from app.models.rsvp import RSVP

router = APIRouter()

@router.post("/", response_model=EventOut)
def create_event(event_in: EventCreate, db: Session = Depends(get_db), current_user=Depends(get_current_organizer)):
    event = Event(**event_in.dict(), organizer_id=current_user.id)
    db.add(event)
    db.commit()
    db.refresh(event)
    return event

@router.get("/", response_model=List[EventOut])
def list_events(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 10,
    date_str: Optional[str] = Query(None, description="Filter by date YYYY-MM-DD"),
    location: Optional[str] = None,
    keyword: Optional[str] = None,
):
    q = db.query(Event)
    if date_str:
        # compare only the date part
        try:
            _ = date.fromisoformat(date_str)
            q = q.filter(func.date(Event.date) == date_str)
        except ValueError:
            raise HTTPException(status_code=400, detail="date must be YYYY-MM-DD")
    if location:
        q = q.filter(Event.location.ilike(f"%{location}%"))
    if keyword:
        q = q.filter(Event.title.ilike(f"%{keyword}%"))
    return q.order_by(Event.date).offset(skip).limit(limit).all()

@router.get("/{event_id}", response_model=EventOut)
def get_event(event_id: int, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

@router.put("/{event_id}", response_model=EventOut)
def update_event(event_id: int, event_in: EventUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_organizer)):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    if event.organizer_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not your event")
    for key, val in event_in.dict(exclude_unset=True).items():
        setattr(event, key, val)
    db.commit()
    db.refresh(event)
    return event

@router.delete("/{event_id}")
def delete_event(event_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_organizer)):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    if event.organizer_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not your event")
    db.delete(event)
    db.commit()
    return {"detail": "Event deleted"}
