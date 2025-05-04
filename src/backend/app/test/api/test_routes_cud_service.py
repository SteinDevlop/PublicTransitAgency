import pytest
from fastapi.testclient import TestClient
from backend.app.api.routes.routes_cud_service import app as routes_router
from backend.app.logic.universal_controller_sql import UniversalController
from backend.app.models.routes import Route
from backend.app.core.conf import headers  # Import headers for authentication
from fastapi import FastAPI
from unittest.mock import patch

# Setup the test application
app_for_test = FastAPI()
app_for_test.include_router(routes_router)
client = TestClient(app_for_test)
controller = UniversalController()

# Mock authentication globally
@pytest.fixture(autouse=True)
def mock_get_current_user():
    with patch("backend.app.core.auth.get_current_user") as mock_user:
        mock_user.return_value = {"user_id": 1, "scopes": ["system", "administrador", "supervisor"]}
        yield mock_user

def setup_function():
    controller.clear_tables()

def teardown_function():
    controller.clear_tables()

def test_crear_ruta():
    """Test that the '/routes/create' route creates a new route."""
    response = client.post("/routes/create", data={
        "ID": 1,
        "IDHorario": 10,
        "Nombre": "Ruta 1"
    }, headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Ruta creada exitosamente."

def test_actualizar_ruta():
    """Test that the '/routes/update' route updates an existing route."""
    controller.add(Route(ID=1, IDHorario=10, Nombre="Ruta 1"))
    response = client.post("/routes/update", data={
        "ID": 1,
        "IDHorario": 20,
        "Nombre": "Ruta Actualizada"
    }, headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Ruta actualizada exitosamente."

def test_eliminar_ruta():
    """Test that the '/routes/delete' route deletes an existing route."""
    controller.add(Route(ID=1, IDHorario=10, Nombre="Ruta 1"))
    response = client.post("/routes/delete", data={"ID": 1}, headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Ruta eliminada exitosamente."