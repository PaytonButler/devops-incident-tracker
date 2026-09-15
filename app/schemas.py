from enum import Enum

from pydantic import BaseModel


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