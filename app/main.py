from fastapi import Depends, FastAPI
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Event
from app.schemas import EventCreate, EventResponse

app = FastAPI()


@app.get("/")
def root():
    return {"message": "DevOps Incident Tracker API"}


@app.get("/events", response_model=list[EventResponse])
def get_events(db: Session = Depends(get_db)):
    statement = select(Event)
    events = db.scalars(statement).all()

    return events


@app.post("/events", response_model=EventResponse)
def create_event(event: EventCreate):
    return {
        "id": 1,
        "service": event.service,
        "level": event.level,
        "message": event.message,
        "response_time": event.response_time
    }