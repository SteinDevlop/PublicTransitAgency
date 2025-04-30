"""from fastapi.testclient import TestClient
from datetime import datetime
from backend.app.api.routes.shifts_cud_service import app
client = TestClient(app)

def test_create_shift():
    response = client.post("/shift/create", data={
        "shift_id": "SHIFT001",
        "unit": "BUS123",
        "start_time": "2025-05-01T08:00:00",
        "end_time": "2025-05-01T12:00:00",
        "driver": "DRIVER001",
        "schedule": "SCHED001"
    })
    assert response.status_code == 200
    assert response.json()["operation"] == "create"
    assert response.json()["success"] is True

def test_update_shift():
    response = client.post("/shift/update", data={
        "shift_id": "SHIFT001",
        "unit": "BUS124",
        "start_time": "2025-05-01T08:30:00",
        "end_time": "2025-05-01T12:30:00",
        "driver": "DRIVER002",
        "schedule": "SCHED002"
    })
    assert response.status_code == 200
    assert response.json()["operation"] == "update"
    assert response.json()["success"] is True

def test_delete_shift():
    response = client.post("/shift/delete", data={
        "shift_id": "SHIFT001"
    })
    assert response.status_code == 200
    assert response.json()["operation"] == "delete"
    assert response.json()["success"] is True
"""