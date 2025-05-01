import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from backend.app.api.routes.shifts_query_service import app
from backend.app.logic.universal_controller_sql import UniversalController
from backend.app.models.shift import ShiftCreate

client = TestClient(app)

def setup_function():
    uc = UniversalController()
    uc.clear_tables()
    # Insertar un turno de prueba
    uc.add(ShiftCreate(
        shift_id="1",
        unit_id="Bus001",
        start_time="2025-05-01T08:00:00",
        end_time="2025-05-01T16:00:00",
        driver_id="Driver001",
        schedule_id="Schedule001"
    ))

def test_list_shifts_page():
    response = client.get("/shifts/listar")
    assert response.status_code == 200
    assert "ListarTurno.html" in response.text

def test_shift_detail_page():
    response = client.get("/shifts/detalles/1")
    assert response.status_code == 200
    assert "DetalleTurno.html" in response.text
    assert "Bus001" in response.text  # Verifica que los datos del turno estén presentes

def test_shift_detail_page_mock():
    mock_controller = MagicMock()
    mock_controller.get_by_id.return_value = {
        "shift_id": "1",
        "unit_id": "Bus001",
        "start_time": "2025-05-01T08:00:00",
        "end_time": "2025-05-01T16:00:00",
        "driver_id": "Driver001",
        "schedule_id": "Schedule001"
    }
    response = client.get("/shifts/detalles/1")
    assert response.status_code == 200
    assert "DetalleTurno.html" in response.text

def test_get_all_shifts():
    response = client.get("/shifts/all")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_shift_by_id():
    response = client.get("/shifts/1")
    assert response.status_code == 200
    data = response.json()
    assert data["shift_id"] == "1"
    assert data["unit_id"] == "Bus001"
    assert data["driver_id"] == "Driver001"

def test_get_shift_by_id_not_found():
    response = client.get("/shifts/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Shift not found"