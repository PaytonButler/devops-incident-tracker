from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root_returns_api_message():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "DevOps Incident Tracker API"
    }

def test_get_events_returns_list():
    response = client.get("/events")

    assert response.status_code == 200
    assert isinstance(response.json(), list)