from fastapi import FastAPI
from pydantic import BaseModel
from enum import Enum

app = FastAPI()

class LogLevel(str, Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class Event(BaseModel):
    service: str
    level: LogLevel
    message: str
    response_time: int


@app.get("/")
def root():
    return {"message": "DevOps Incident Tracker API"}


@app.get("/events")
def get_events():
    return {"events": []}


@app.post("/events")
def create_event(event: Event):
    return event