from fastapi.testclient import TestClient
from backend.app.api.routes.incidence_query_service import app as incidences_router
from backend.app.logic.universal_controller_sql import UniversalController
from backend.app.models.incidence import Incidence
from fastapi import FastAPI
from unittest.mock import patch
import pytest
from backend.app.core.conf import headers  # Import headers for authentication

# Setup the test application
app_for_test = FastAPI()
app_for_test.include_router(incidences_router)
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

def test_listar_incidencias():
    """Test that the '/incidences/' route lists all incidences."""
    controller.add(Incidence(ID=1, IDTicket=1, Descripcion="Test", Tipo="Tipo1", IDUnidad=1))
    response = client.get("/incidences/", headers=headers)
    assert response.status_code == 200
    assert "Test" in response.text

def test_detalle_incidencia_existente():
    """Test that the '/incidences/{id}' route retrieves an existing incidence."""
    controller.add(Incidence(ID=1, IDTicket=1, Descripcion="Test", Tipo="Tipo1", IDUnidad=1))
    response = client.get("/incidences/1", headers=headers)
    assert response.status_code == 200
    assert "Test" in response.text

def test_detalle_incidencia_no_existente():
    """Test that the '/incidences/{id}' route returns 404 for a non-existent incidence."""
    response = client.get("/incidences/999", headers=headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "Incidencia no encontrada"