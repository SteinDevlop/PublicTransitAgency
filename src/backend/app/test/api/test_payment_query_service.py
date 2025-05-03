from fastapi.testclient import TestClient
from backend.app.api.routes.payment_query_service import app as payments_router
from backend.app.logic.universal_controller_sql import UniversalController
from backend.app.models.payments import Payment
from fastapi import FastAPI

app_for_test = FastAPI()
app_for_test.include_router(payments_router)
client = TestClient(app_for_test)
controller = UniversalController()

def setup_function():
    controller.clear_tables()

def teardown_function():
    controller.clear_tables()

def test_listar_pagos():
    response = client.get("/payments/")
    assert response.status_code == 200

def test_detalle_pago_existente():
    controller.add(Payment(id=1, user="Juan", payment_quantity=100.0, payment_method=True, vehicle_type=1, card_id=123))
    response = client.get("/payments/1")
    assert response.status_code == 200

def test_detalle_pago_no_existente():
    # Intentar consultar un pago en una tabla vacía
    response = client.get("/payments/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Pago no encontrado"