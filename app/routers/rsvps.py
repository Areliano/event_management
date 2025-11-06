# app/routers/rsvps.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.auth import get_current_user, get_current_organizer
from app.schemas.rsvp import RSVPCreate, RSVPOut
from app.models.event import Event
from app.models.rsvp import RSVP

router = APIRouter()

@router.post("/", response_model=RSVPOut)
def create_rsvp(rsvp_in: RSVPCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    event = db.query(Event).filter(Event.id == rsvp_in.event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    # Check if user already RSVPed
    existing = db.query(RSVP).filter(RSVP.event_id == rsvp_in.event_id, RSVP.user_id == current_user.id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Already RSVPed for this event")

    # Count existing RSVPs (total)
    count = db.query(RSVP).filter(RSVP.event_id == rsvp_in.event_id).count()
    if count >= event.max_attendees:
        raise HTTPException(status_code=400, detail="Event is full")

    rsvp = RSVP(user_id=current_user.id, event_id=rsvp_in.event_id)
    db.add(rsvp)
    db.commit()
    db.refresh(rsvp)
    return rsvp

@router.get("/my", response_model=List[RSVPOut])
def my_rsvps(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    rsvps = db.query(RSVP).filter(RSVP.user_id == current_user.id).all()
    return rsvps

@router.get("/event/{event_id}", response_model=List[RSVPOut])
def event_rsvps(event_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_organizer)):
    # organizer only — verify organizer owns the event
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    if event.organizer_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not your event")
    rsvps = db.query(RSVP).filter(RSVP.event_id == event_id).all()
    return rsvps

@router.put("/{rsvp_id}/approve", response_model=RSVPOut)
def approve_rsvp(rsvp_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_organizer)):
    rsvp = db.query(RSVP).filter(RSVP.id == rsvp_id).first()
    if not rsvp:
        raise HTTPException(status_code=404, detail="RSVP not found")

    # make sure organizer owns the event
    event = db.query(Event).filter(Event.id == rsvp.event_id).first()
    if not event or event.organizer_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not permitted to approve")

    rsvp.approved = True
    db.commit()
    db.refresh(rsvp)
    return rsvp
