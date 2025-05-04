from fastapi.testclient import TestClient
from backend.app.api.routes.maintainance_status_query_service import app as maintainance_router
from backend.app.logic.universal_controller_sql import UniversalController
from backend.app.models.maintainance_status import MaintainanceStatus
from fastapi import FastAPI
from unittest.mock import patch
import pytest
from backend.app.core.conf import headers  # Import headers for authentication

# Setup the test application
app_for_test = FastAPI()
app_for_test.include_router(maintainance_router)
client = TestClient(app_for_test)
controller = UniversalController()

# Mock authentication globally
@pytest.fixture(autouse=True)
def mock_get_current_user():
    with patch("backend.app.core.auth.get_current_user") as mock_user:
        mock_user.return_value = {"user_id": 1, "scopes": ["system", "mantenimiento", "supervisor"]}
        yield mock_user

def setup_function():
    controller.clear_tables()

def teardown_function():
    controller.clear_tables()

def test_listar_estados():
    """Test that the '/maintainance_status/' route lists all maintenance statuses."""
    controller.add(MaintainanceStatus(id=1, unit="Unit1", type="Type1", status="Active"))
    response = client.get("/maintainance_status/", headers=headers)
    assert response.status_code == 200
    assert "Unit1" in response.text

def test_detalle_estado_existente():
    """Test that the '/maintainance_status/{id}' route retrieves an existing maintenance status."""
    controller.add(MaintainanceStatus(id=1, unit="Unit1", type="Type1", status="Active"))
    response = client.get("/maintainance_status/1", headers=headers)
    assert response.status_code == 200
    assert "Unit1" in response.text

def test_detalle_estado_no_existente():
    """Test that the '/maintainance_status/{id}' route returns 404 for a non-existent maintenance status."""
    response = client.get("/maintainance_status/999", headers=headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "Estado de mantenimiento no encontrado"