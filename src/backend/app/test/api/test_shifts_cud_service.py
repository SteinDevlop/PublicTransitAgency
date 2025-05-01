import pytest
from fastapi.testclient import TestClient
from backend.app.api.routes.shifts_query_service import app

client = TestClient(app)

def test_index_create():
    response = client.get("/shifts/crear")
    assert response.status_code == 200
    assert "CrearTurno.html" in response.text

def test_index_update():
    response = client.get("/shifts/actualizar")
    assert response.status_code == 200
    assert "ActualizarTurno.html" in response.text

def test_index_delete():
    response = client.get("/shifts/eliminar")
    assert response.status_code == 200
    assert "EliminarTurno.html" in response.text

def test_create_shift():
    data = {
        "shift_id": "1",
        "unit": "Bus123",
        "start_time": "2025-05-01T08:00:00",
        "end_time": "2025-05-01T16:00:00",
        "driver": "Driver1",
        "schedule": "Schedule1"
    }
    response = client.post("/shifts/create", data=data)
    assert response.status_code == 200
    assert response.json()["operation"] == "create"
    assert response.json()["success"] is True

def test_update_shift():
    data = {
        "unit": "Bus456",
        "start_time": "2025-05-01T09:00:00",
        "end_time": "2025-05-01T17:00:00"
    }
    response = client.post("/shifts/update/1", data=data)
    assert response.status_code == 200
    assert response.json()["operation"] == "update"
    assert response.json()["success"] is True

def test_delete_shift():
    response = client.post("/shifts/delete/1")
    assert response.status_code == 200
    assert response.json()["operation"] == "delete"
    assert response.json()["success"] is True