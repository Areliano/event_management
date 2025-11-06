# app/main.py
from fastapi import FastAPI
from app.core.database import Base, engine
from app.models import user, event
from app.routers import auth, events

app = FastAPI(title="Event Management System")

# Create all tables in the database
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(events.router, prefix="/events", tags=["Events"])

@app.get("/")
def root():
    return {"message": "Welcome to the Event Management System API"}
