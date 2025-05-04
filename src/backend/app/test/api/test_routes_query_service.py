import pytest
from fastapi.testclient import TestClient
from backend.app.api.routes.routes_query_service import app as routes_router
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

def test_listar_rutas():
    """Test that the '/routes/' route lists all routes."""
    controller.add(Route(ID=1, IDHorario=10, Nombre="Ruta 1"))
    response = client.get("/routes/", headers=headers)
    assert response.status_code == 200
    assert "Ruta 1" in response.text

def test_detalle_ruta_existente():
    """Test that the '/routes/{ID}' route retrieves an existing route."""
    controller.add(Route(ID=1, IDHorario=10, Nombre="Ruta 1"))
    response = client.get("/routes/1", headers=headers)
    assert response.status_code == 200
    assert "Ruta 1" in response.text

def test_detalle_ruta_no_existente():
    """Test that the '/routes/{ID}' route returns 404 for a non-existent route."""
    response = client.get("/routes/999", headers=headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "Ruta no encontrada"