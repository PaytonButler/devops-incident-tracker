from fastapi import Depends, FastAPI
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Event
from app.schemas import EventCreate, EventResponse, LogLevel

app = FastAPI()


@app.get("/")
def root():
    return {"message": "DevOps Incident Tracker API"}


@app.get("/events", response_model=list[EventResponse])
def get_events(
    level: LogLevel | None = None,
    service: str | None = None,
    db: Session = Depends(get_db)
):
    statement = select(Event)

    if level is not None:
        statement = statement.where(Event.level == level.value)

    if service is not None:
        statement = statement.where(Event.service == service)

    events = db.scalars(statement).all()

    return events


@app.post("/events", response_model=EventResponse)
def create_event(
    event: EventCreate,
    db: Session = Depends(get_db)
):
    db_event = Event(
        service=event.service,
        level=event.level.value,
        message=event.message,
        response_time=event.response_time
    )

    try:
        db.add(db_event)
        db.commit()
        db.refresh(db_event)
    except Exception:
        db.rollback()
        raise

    return db_event