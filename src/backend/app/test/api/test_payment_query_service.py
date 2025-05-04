import pytest
from fastapi.testclient import TestClient
from backend.app.api.routes.payment_query_service import app as payments_router
from backend.app.logic.universal_controller_sql import UniversalController
from backend.app.models.payments import Payment
from backend.app.core.conf import headers  # Import headers for authentication
from fastapi import FastAPI
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

def test_listar_pagos():
    """Test that the '/payments/' route lists all payments."""
    controller.add(Payment(id=1, user="Juan", payment_quantity=100.0, payment_method=True, vehicle_type=1, card_id=123))
    response = client.get("/payments/", headers=headers)
    assert response.status_code == 200
    assert "Juan" in response.text

def test_detalle_pago_existente():
    """Test that the '/payments/{id}' route retrieves an existing payment."""
    controller.add(Payment(id=1, user="Juan", payment_quantity=100.0, payment_method=True, vehicle_type=1, card_id=123))
    response = client.get("/payments/1", headers=headers)
    assert response.status_code == 200
    assert "Juan" in response.text

def test_detalle_pago_no_existente():
    """Test that the '/payments/{id}' route returns 404 for a non-existent payment."""
    response = client.get("/payments/999", headers=headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "Pago no encontrado"