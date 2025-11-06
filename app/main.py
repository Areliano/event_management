# app/main.py
from fastapi import FastAPI
from app.core.database import Base, engine
from app.routers import auth, events, rsvps  # import packages

# create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Event Management System API")

# include routers with a single prefix each
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(events.router, prefix="/events", tags=["Events"])
app.include_router(rsvps.router, prefix="/rsvps", tags=["RSVPs"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Event Management System API"}
