from sqlalchemy import String, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True)
    service: Mapped[str] = mapped_column(String(100))
    level: Mapped[str] = mapped_column(String(20))
    message: Mapped[str] = mapped_column(String(500))
    response_time: Mapped[int]


engine = create_engine("sqlite:///incident_tracker.db")

Base.metadata.create_all(engine)