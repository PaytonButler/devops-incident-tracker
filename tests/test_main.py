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

def test_filter_events_by_level(client):
    client.post("/events", json={
        "service": "payment-service",
        "level": "ERROR",
        "message": "Payment failed",
        "response_time": 3000
    })

    client.post("/events", json={
        "service": "auth-service",
        "level": "INFO",
        "message": "User logged in",
        "response_time": 200
    })

    response = client.get("/events", params={"level": "ERROR"})

    assert response.status_code == 200
    events = response.json()

    assert len(events) == 1
    assert events[0]["level"] == "ERROR"


def test_filter_events_by_service(client):
    client.post("/events", json={
        "service": "payment-service",
        "level": "ERROR",
        "message": "Payment failed",
        "response_time": 3000
    })

    client.post("/events", json={
        "service": "auth-service",
        "level": "INFO",
        "message": "User logged in",
        "response_time": 200
    })

    response = client.get(
        "/events",
        params={"service": "payment-service"}
    )

    assert response.status_code == 200
    events = response.json()

    assert len(events) == 1
    assert events[0]["service"] == "payment-service"


def test_filter_events_by_level_and_service(client):
    client.post("/events", json={
        "service": "payment-service",
        "level": "ERROR",
        "message": "Payment failed",
        "response_time": 3000
    })

    client.post("/events", json={
        "service": "payment-service",
        "level": "INFO",
        "message": "Payment processed",
        "response_time": 200
    })

    client.post("/events", json={
        "service": "auth-service",
        "level": "ERROR",
        "message": "Login failed",
        "response_time": 500
    })

    response = client.get(
        "/events",
        params={
            "level": "ERROR",
            "service": "payment-service"
        }
    )

    assert response.status_code == 200
    events = response.json()

    assert len(events) == 1
    assert events[0]["level"] == "ERROR"
    assert events[0]["service"] == "payment-service"

def test_get_events_returns_empty_list_when_no_events_exist(client):
    response = client.get("/events")

    assert response.status_code == 200
    assert response.json() == []


def test_filter_events_returns_empty_list_when_no_match(client):
    response = client.get(
        "/events",
        params={"service": "nonexistent-service"}
    )

    assert response.status_code == 200
    assert response.json() == []


def test_filter_events_rejects_invalid_level(client):
    response = client.get(
        "/events",
        params={"level": "BANANA"}
    )

    assert response.status_code == 422

def test_create_event_rejects_negative_response_time(client):
    payload = {
        "service": "payment-service",
        "level": "ERROR",
        "message": "Invalid response time",
        "response_time": -500
    }

    response = client.post("/events", json=payload)

    assert response.status_code == 422

def test_create_event_rejects_missing_message(client):
    payload = {
        "service": "payment-service",
        "level": "ERROR",
        "response_time": 500
    }

    response = client.post("/events", json=payload)

    assert response.status_code == 422


def test_error_event_creates_incident(client):
    payload = {
        "service": "payment-service",
        "level": "ERROR",
        "message": "Database connection failed",
        "response_time": 3500
    }

    event_response = client.post("/events", json=payload)

    assert event_response.status_code == 200

    incident_response = client.get("/incidents")

    assert incident_response.status_code == 200
    incidents = incident_response.json()

    assert len(incidents) == 1
    assert incidents[0]["event_id"] == event_response.json()["id"]
    assert incidents[0]["service"] == "payment-service"
    assert incidents[0]["level"] == "ERROR"


def test_info_event_does_not_create_incident(client):
    payload = {
        "service": "auth-service",
        "level": "INFO",
        "message": "User logged in",
        "response_time": 150
    }

    event_response = client.post("/events", json=payload)

    assert event_response.status_code == 200

    incident_response = client.get("/incidents")

    assert incident_response.status_code == 200
    assert incident_response.json() == []