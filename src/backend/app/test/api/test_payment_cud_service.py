from fastapi.testclient import TestClient
from backend.app.api.routes.payment_CUD_service import app as payments_router
from backend.app.logic.universal_controller_sql import UniversalController
from backend.app.models.payments import Payment
from fastapi import FastAPI
from backend.app.core.conf import headers  # Import headers for authentication
import pytest
from unittest.mock import patch

# Setup the test application
app_for_test = FastAPI()
app_for_test.include_router(payments_router)
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

def test_crear_pago():
    """Test that the '/payments/create' route creates a new payment."""
    response = client.post("/payments/create", data={
        "id": 1,
        "user": "Juan",
        "payment_quantity": 100.0,
        "payment_method": True,
        "vehicle_type": 1,
        "card_id": 123
    }, headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Pago creado exitosamente."

def test_actualizar_pago():
    """Test that the '/payments/update' route updates an existing payment."""
    controller.add(Payment(id=1, user="Juan", payment_quantity=100.0, payment_method=True, vehicle_type=1, card_id=123))
    response = client.post("/payments/update", data={
        "id": 1,
        "user": "Juan",
        "payment_quantity": 150.0,
        "payment_method": False,
        "vehicle_type": 2,
        "card_id": 123
    }, headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Pago actualizado exitosamente."

def test_actualizar_pago_no_existente():
    """Test that the '/payments/update' route returns 404 for a non-existent payment."""
    response = client.post("/payments/update", data={
        "id": 999,
        "user": "Juan",
        "payment_quantity": 150.0,
        "payment_method": False,
        "vehicle_type": 2,
        "card_id": 123
    }, headers=headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "Pago no encontrado"

def test_eliminar_pago():
    """Test that the '/payments/delete' route deletes an existing payment."""
    controller.add(Payment(id=1, user="Juan", payment_quantity=100.0, payment_method=True, vehicle_type=1, card_id=123))
    response = client.post("/payments/delete", data={"id": 1}, headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Pago eliminado exitosamente."

def test_eliminar_pago_no_existente():
    """Test that the '/payments/delete' route returns 404 for a non-existent payment."""
    response = client.post("/payments/delete", data={"id": 999}, headers=headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "Pago no encontrado"