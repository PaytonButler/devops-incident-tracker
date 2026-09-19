from sqlalchemy import select

from app.models import Event, SessionLocal

db = SessionLocal()

try:
    statement = select(Event)
    events = db.scalars(statement).all()

    for event in events:
        print(
            event.id,
            event.service,
            event.level,
            event.message,
            event.response_time
        )

finally:
    db.close()