from enum import Enum

from pydantic import BaseModel


class LogLevel(str, Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class EventCreate(BaseModel):
    service: str
    level: LogLevel
    message: str
    response_time: int


class EventResponse(BaseModel):
    id: int
    service: str
    level: LogLevel
    message: str
    response_time: int