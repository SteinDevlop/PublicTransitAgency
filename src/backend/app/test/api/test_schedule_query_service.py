import pytest
from fastapi.testclient import TestClient
from backend.app.api.routes.schedule_query_service import app as schedules_router
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

def test_listar_horarios():
    controller.add(Schedule(ID=1, Llegada="08:00:00", Salida="10:00:00"))
    response = client.get("/schedules/", headers=headers)
    assert response.status_code == 200
    assert "08:00:00" in response.text

def test_detalle_horario_existente():
    controller.add(Schedule(ID=1, Llegada="08:00:00", Salida="10:00:00"))
    response = client.get("/schedules/1", headers=headers)
    assert response.status_code == 200
    assert "08:00:00" in response.text

def test_detalle_horario_no_existente():
    response = client.get("/schedules/999", headers=headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "Horario no encontrado"