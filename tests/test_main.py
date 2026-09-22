def test_root_returns_api_message(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "DevOps Incident Tracker API"
    }


def test_get_events_returns_list(client):
    response = client.get("/events")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_event_persists_to_database(client):
    payload = {
        "service": "payment-service",
        "level": "ERROR",
        "message": "Database connection failed",
        "response_time": 3500
    }

    create_response = client.post("/events", json=payload)

    assert create_response.status_code == 200

    created_event = create_response.json()
    assert created_event["id"] is not None
    assert created_event["service"] == "payment-service"

    get_response = client.get("/events")

    assert get_response.status_code == 200
    events = get_response.json()

    assert len(events) == 1
    assert events[0]["id"] == created_event["id"]
    assert events[0]["message"] == "Database connection failed"

def test_create_event_rejects_invalid_level(client):
    payload = {
        "service": "payment-service",
        "level": "BANANA",
        "message": "Invalid log level",
        "response_time": 100
    }

    response = client.post("/events", json=payload)

    assert response.status_code == 422