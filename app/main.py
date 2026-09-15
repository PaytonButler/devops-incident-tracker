from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return {"message": "DevOps Incident Tracker API"}


@app.get("/events")
def get_events():
    return {"events": []}