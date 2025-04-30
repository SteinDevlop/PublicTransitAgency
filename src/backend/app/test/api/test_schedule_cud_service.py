"""from fastapi.testclient import TestClient
from datetime import datetime, timedelta
from backend.app.api.routes.schedule_cud_service import app

client = TestClient(app)

def test_create_schedule_success():
    payload = {
        "schedule_id": "test_schedule_001",
        "arrival_date": (datetime.now() + timedelta(days=1)).isoformat(),
        "departure_date": (datetime.now() + timedelta(days=2)).isoformat(),
        "route": "route_001"
    }
    response = client.post("/schedule/create", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["operation"] == "create"
    assert data["success"] is True
    assert "data" in data
    assert data["message"] == "Schedule created successfully"

def test_update_schedule_success():
    payload = {
        "schedule_id": "test_schedule_001",
        "arrival_date": (datetime.now() + timedelta(days=3)).isoformat(),
        "departure_date": (datetime.now() + timedelta(days=4)).isoformat(),
        "route": "route_002"
    }
    response = client.post("/schedule/update", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["operation"] == "update"
    assert data["success"] is True
    assert data["data"]["schedule_id"] == "test_schedule_001"
    assert data["message"] == "Schedule test_schedule_001 updated"

def test_delete_schedule_success():
    payload = {
        "schedule_id": "test_schedule_001"
    }
    response = client.post("/schedule/delete", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["operation"] == "delete"
    assert data["success"] is True
    assert data["message"] == "Schedule test_schedule_001 deleted"

def test_delete_schedule_not_found():
    payload = {
        "schedule_id": "non_existing_schedule"
    }
    response = client.post("/schedule/delete", json=payload)
    assert response.status_code == 404
    assert response.json()["detail"] == "Schedule not found"
"""