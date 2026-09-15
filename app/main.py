from fastapi import FastAPI

from app.schemas import EventCreate, EventResponse

app = FastAPI()


@app.get("/")
def root():
    return {"message": "DevOps Incident Tracker API"}


@app.get("/events")
def get_events():
    return {"events": []}


@app.post("/events", response_model=EventResponse)
def create_event(event: EventCreate):
    return {
        "id": 1,
        "service": event.service,
        "level": event.level,
        "message": event.message,
        "response_time": event.response_time
    }