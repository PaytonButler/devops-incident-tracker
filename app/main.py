from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.incident_rules import is_incident, is_high_latency
from app.models import Event, Incident
from app.schemas import EventCreate, EventResponse, IncidentResponse, LogLevel, IncidentStatus

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

        # Insert the event so it receives a database ID.
        db.flush()

        # Create an incident if the event's level triggers the rule.
        if (is_incident(db_event.level) or is_high_latency(db_event.response_time)):
            db_incident = Incident(
                event_id=db_event.id,
                service=db_event.service,
                level=db_event.level,
                message=db_event.message
            )
            db.add(db_incident)

        # Save the event and any incident together.
        db.commit()
        db.refresh(db_event)

    except Exception:
        db.rollback()
        raise

    return db_event


@app.get("/incidents", response_model=list[IncidentResponse])
def get_incidents(
    status: IncidentStatus | None = None,
    db: Session = Depends(get_db)
):
    statement = select(Incident)

    if status is not None:
        statement = statement.where(Incident.status == status.value)

    incidents = db.scalars(statement).all()

    return incidents


@app.patch("/incidents/{incident_id}/resolve",
           response_model=IncidentResponse)
def resolve_incident(
    incident_id: int,
    db: Session = Depends(get_db)
):
    incident = db.get(Incident, incident_id)

    if incident is None:
        raise HTTPException(
            status_code=404,
            detail="Incident not found"
        )

    incident.status = IncidentStatus.RESOLVED.value

    db.commit()
    db.refresh(incident)

    return incident