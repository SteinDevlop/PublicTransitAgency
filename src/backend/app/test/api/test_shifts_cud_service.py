import pytest
from fastapi.testclient import TestClient
from backend.app.api.routes.shifts_CUD_service import app as shifts_router
from backend.app.logic.universal_controller_sql import UniversalController
from backend.app.models.shift import Shift
from backend.app.core.conf import headers  # Import headers for authentication
from fastapi import FastAPI
from unittest.mock import patch

app_for_test = FastAPI()
app_for_test.include_router(shifts_router)
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

def test_crear_turno():
    response = client.post("/shifts/create", data={
        "ID": 1,
        "TipoTurno": "Diurno"
    }, headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Turno creado exitosamente."

def test_actualizar_turno():
    controller.add(Shift(ID=1, TipoTurno="Diurno"))
    response = client.post("/shifts/update", data={
        "ID": 1,
        "TipoTurno": "Nocturno"
    }, headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Turno actualizado exitosamente."

def test_eliminar_turno():
    controller.add(Shift(ID=1, TipoTurno="Diurno"))
    response = client.post("/shifts/delete", data={"ID": 1}, headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Turno eliminado exitosamente."