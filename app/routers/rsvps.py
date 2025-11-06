from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.auth import get_current_user, get_current_organizer
from app.models.event import Event, RSVP
from app.schemas.event import RSVPCreate, RSVPOut

router = APIRouter(prefix="/rsvp", tags=["RSVPs"])

@router.post("/", response_model=RSVPOut)
def create_rsvp(
    rsvp: RSVPCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    event = db.query(Event).filter(Event.id == rsvp.event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    count = db.query(RSVP).filter(RSVP.event_id == rsvp.event_id).count()
    if count >= event.max_attendees:
        raise HTTPException(status_code=400, detail="Event full")

    existing = db.query(RSVP).filter(
        RSVP.event_id == rsvp.event_id, RSVP.user_id == current_user.id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Already RSVPed")

    new_rsvp = RSVP(event_id=rsvp.event_id, user_id=current_user.id)
    db.add(new_rsvp)
    db.commit()
    db.refresh(new_rsvp)
    return new_rsvp

@router.put("/{rsvp_id}/approve", response_model=RSVPOut)
def approve_rsvp(
    rsvp_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_organizer)
):
    rsvp = db.query(RSVP).filter(RSVP.id == rsvp_id).first()
    if not rsvp:
        raise HTTPException(status_code=404, detail="RSVP not found")
    rsvp.approved = True
    db.commit()
    db.refresh(rsvp)
    return rsvp
