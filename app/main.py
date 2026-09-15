from fastapi import FastAPI

from app.schemas import Event

app = FastAPI()


@app.get("/")
def root():
    return {"message": "DevOps Incident Tracker API"}


@app.get("/events")
def get_events():
    return {"events": []}


@app.post("/events")
def create_event(event: Event):
    return event