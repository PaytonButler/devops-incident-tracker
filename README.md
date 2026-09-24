
# DevOps Incident Tracker

A Python backend application that ingests service events, detects potential incidents, and tracks incident resolution.

## Features

- Ingest service events through a REST API
- Validate event severity and response time
- Automatically create incidents for ERROR and CRITICAL events
- Detect high-latency events exceeding 2000 ms
- Filter events by service and severity
- Filter incidents by status
- Resolve incidents through the API
- Persist data using SQLite and SQLAlchemy
- Run the application in Docker with persistent database storage

## Tech Stack

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pytest
- Docker

## Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/PaytonButler/devops-incident-tracker.git
cd devops-incident-tracker
```

### 2. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Start the API

```bash
python -m uvicorn app.main:app --reload
```

Swagger UI: http://localhost:8000/docs

## Run with Docker

Build the image:

```bash
docker build -t incident-tracker .
```

Create a persistent volume:

```bash
docker volume create incident-data
```

Run the container:

```bash
docker run -d --name incident-tracker-app -p 8000:8000 -e DATABASE_URL=sqlite:////data/incident_tracker.db -v incident-data:/data incident-tracker
```

The named volume stores the SQLite database independently of the container lifecycle.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Root endpoint |
| GET | `/events` | List and filter events |
| POST | `/events` | Ingest an event |
| GET | `/incidents` | List and filter incidents |
| PATCH | `/incidents/{incident_id}/resolve` | Resolve an incident |

## Run Tests

```bash
python -m pytest -v
```

The test suite covers API behavior, input validation, event filtering, incident detection, and incident resolution.

## Incident Detection Rules

An incident is created when either condition is met:

- Event severity is `ERROR` or `CRITICAL`
- Response time exceeds 2000 milliseconds

New incidents are assigned the `OPEN` status. They can later be marked `RESOLVED`.

## Project Purpose

This project was built to strengthen practical Python backend development skills, including REST API design, database integration, automated testing, debugging, Git workflows, and containerization.