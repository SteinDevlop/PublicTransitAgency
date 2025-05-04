import pytest
from fastapi.testclient import TestClient
from backend.app.api.routes.schedule_cud_service import app as schedules_router
from backend.app.logic.universal_controller_sql import UniversalController
from backend.app.models.schedule import Schedule
from backend.app.core.conf import headers  # Import headers for authentication
from fastapi import FastAPI
from unittest.mock import patch

app_for_test = FastAPI()
app_for_test.include_router(schedules_router)
client = TestClient(app_for_test)
controller = UniversalController()

@pytest.fixture(autouse=True)
def mock_get_current_user():
    with patch("backend.app.core.auth.get_current_user") as mock_user:
        mock_user.return_value = {"user_id": 1, "scopes": ["system", "administrador", "supervisor"]}
        yield mock_user

def setup_function():
    controller.clear_tables()

def teardown_function():
    controller.clear_tables()

def test_crear_horario():
    response = client.post("/schedules/create", data={
        "ID": 1,
        "Llegada": "08:00:00",
        "Salida": "10:00:00"
    }, headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Horario creado exitosamente."

def test_actualizar_horario():
    controller.add(Schedule(ID=1, Llegada="08:00:00", Salida="10:00:00"))
    response = client.post("/schedules/update", data={
        "ID": 1,
        "Llegada": "09:00:00",
        "Salida": "11:00:00"
    }, headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Horario actualizado exitosamente."

def test_eliminar_horario():
    controller.add(Schedule(ID=1, Llegada="08:00:00", Salida="10:00:00"))
    response = client.post("/schedules/delete", data={"ID": 1}, headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Horario eliminado exitosamente."