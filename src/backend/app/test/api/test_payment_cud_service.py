from fastapi import FastAPI
from fastapi.testclient import TestClient
from backend.app.logic.universal_controller_sql import UniversalController
from src.backend.app.api.routes.payment_query_service import app as payment_router

def setup_function():
    UniversalController().clear_tables()

def teardown_function():
    UniversalController().clear_tables()

app_for_test = FastAPI()
app_for_test.include_router(payment_router)
client = TestClient(app_for_test)

def test_create_payment():
    response = client.post(
        "/payments/create",
        data={
            "user": "test_user",
            "payment_quantity": 10.50,
            "payment_method": True,
            "vehicle_type": 1,
            "card_id": 123
        }
    )
    assert response.status_code == 200
    assert response.json()["success"] is True
    assert response.json()["data"]["user"] == "test_user"

def test_update_payment_existing():
    # Crear un pago primero
    client.post(
        "/payments/create",
        data={
            "user": "old_user",
            "payment_quantity": 5.00,
            "payment_method": False,
            "vehicle_type": 2,
            "card_id": 456
        }
    )
    # Luego actualizarlo
    response = client.post(
        "/payments/update/1", # Assuming ID 1 was created
        data={
            "user": "new_user",
            "payment_quantity": 7.50,
            "payment_method": True,
            "vehicle_type": 3,
            "card_id": 789
        }
    )
    assert response.status_code == 200
    assert response.json()["success"] is True
    assert response.json()["data"]["user"] == "new_user"

def test_update_payment_not_found():
    response = client.post(
        "/payments/update/999",
        data={
            "user": "nonexistent_user",
            "payment_quantity": 1.00,
            "payment_method": False,
            "vehicle_type": 4,
            "card_id": 101
        }
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Payment not found"

def test_delete_payment_existing():
    # Crear un pago primero
    client.post(
        "/payments/create",
        data={
            "user": "to_delete",
            "payment_quantity": 2.00,
            "payment_method": True,
            "vehicle_type": 5,
            "card_id": 202
        }
    )
    # Luego eliminarlo
    response = client.post("/payments/delete/1") # Assuming ID 1 was created
    assert response.status_code == 200
    assert response.json()["success"] is True

def test_delete_payment_not_found():
    response = client.post("/payments/delete/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Payment not found"

def test_index_create_form():
    response = client.get("/payments/crear")
    assert response.status_code == 200

def test_index_update_form():
    response = client.get("/payments/actualizar")
    assert response.status_code == 200

def test_index_delete_form():
    response = client.get("/payments/eliminar")
    assert response.status_code == 200 