from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class LogLevel(str, Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class EventCreate(BaseModel):
    service: str
    level: LogLevel
    message: str
    response_time: int = Field(ge=0)


class EventResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    service: str
    level: LogLevel
    message: str
    response_time: int

class IncidentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    event_id: int
    service: str
    level: LogLevel
    message: str