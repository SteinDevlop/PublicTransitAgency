from fastapi.testclient import TestClient
from backend.app.api.routes.maintainance_status_CUD_service import app as maintainance_router
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
        mock_user.return_value = {"user_id": 1, "scopes": ["system", "mantenimiento"]}
        yield mock_user

def setup_function():
    controller.clear_tables()

def teardown_function():
    controller.clear_tables()

def test_crear_estado():
    """Test that the '/maintainance_status/create' route creates a new maintenance status."""
    response = client.post("/maintainance_status/create", data={
        "id": 1,
        "unit": "Unit1",
        "type": "Type1",
        "status": "Active"
    }, headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Estado de mantenimiento creado exitosamente."

def test_actualizar_estado():
    """Test that the '/maintainance_status/update' route updates an existing maintenance status."""
    controller.add(MaintainanceStatus(id=1, unit="Unit1", type="Type1", status="Active"))
    response = client.post("/maintainance_status/update", data={
        "id": 1,
        "unit": "Unit1",
        "type": "Type2",
        "status": "Inactive"
    }, headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Estado de mantenimiento actualizado exitosamente."

def test_actualizar_estado_no_existente():
    """Test that the '/maintainance_status/update' route returns 404 for a non-existent maintenance status."""
    response = client.post("/maintainance_status/update", data={
        "id": 999,
        "unit": "Unit1",
        "type": "Type1",
        "status": "Active"
    }, headers=headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "Estado de mantenimiento no encontrado"

def test_eliminar_estado():
    """Test that the '/maintainance_status/delete' route deletes an existing maintenance status."""
    controller.add(MaintainanceStatus(id=1, unit="Unit1", type="Type1", status="Active"))
    response = client.post("/maintainance_status/delete", data={"id": 1}, headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Estado de mantenimiento eliminado exitosamente."

def test_eliminar_estado_no_existente():
    """Test that the '/maintainance_status/delete' route returns 404 for a non-existent maintenance status."""
    response = client.post("/maintainance_status/delete", data={"id": 999}, headers=headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "Estado de mantenimiento no encontrado"