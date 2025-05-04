import pytest
from fastapi.testclient import TestClient
from backend.app.api.routes.stops_cud_service import app as stops_router
from backend.app.logic.universal_controller_sql import UniversalController
from backend.app.models.stops import Stop
from backend.app.core.conf import headers  # Import headers for authentication
from fastapi import FastAPI
from unittest.mock import patch

app_for_test = FastAPI()
app_for_test.include_router(stops_router)
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

def test_crear_parada():
    response = client.post("/stops/create", data={
        "ID": 1,
        "Nombre": "Parada 1",
        "Ubicacion": "Ubicación 1"
    }, headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Parada creada exitosamente."

def test_actualizar_parada():
    controller.add(Stop(ID=1, Nombre="Parada 1", Ubicacion="Ubicación 1"))
    response = client.post("/stops/update", data={
        "ID": 1,
        "Nombre": "Parada Actualizada",
        "Ubicacion": "Ubicación Actualizada"
    }, headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Parada actualizada exitosamente."

def test_eliminar_parada():
    controller.add(Stop(ID=1, Nombre="Parada 1", Ubicacion="Ubicación 1"))
    response = client.post("/stops/delete", data={"ID": 1}, headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Parada eliminada exitosamente."