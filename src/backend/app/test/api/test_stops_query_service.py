import pytest
from fastapi.testclient import TestClient
from backend.app.api.routes.stops_query_service import app as stops_router
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

def test_listar_paradas():
    controller.add(Stop(ID=1, Nombre="Parada 1", Ubicacion="Ubicación 1"))
    response = client.get("/stops/", headers=headers)
    assert response.status_code == 200
    assert "Parada 1" in response.text

def test_detalle_parada_existente():
    controller.add(Stop(ID=1, Nombre="Parada 1", Ubicacion="Ubicación 1"))
    response = client.get("/stops/1", headers=headers)
    assert response.status_code == 200
    assert "Parada 1" in response.text

def test_detalle_parada_no_existente():
    response = client.get("/stops/999", headers=headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "Parada no encontrada"