from fastapi import FastAPI
from fastapi.testclient import TestClient
from backend.app.api.routes.payment_CUD_service import app as payment_router
from backend.app.logic.universal_controller_sql import UniversalController
from backend.app.models.payments import PaymentCreate, PaymentOut
import pytest
import datetime

# Limpieza de la base de datos antes y después de cada prueba
@pytest.fixture(scope="module")
def test_db():
    UniversalController().clear_tables()
    yield
    UniversalController().clear_tables()

# Creamos la aplicación de prueba
app_for_test = FastAPI()
app_for_test.include_router(payment_router)  # Incluye el router
client = TestClient(app_for_test)
controller = UniversalController()

def test_create_payment(test_db):
    """Prueba la creación de un pago."""
    now = datetime.datetime.now()
    payment_data = {
        "date": now.isoformat(),
        "user": "test_user",
        "payment_quantity": 10.50,
        "payment_method": True,
        "vehicle_type": 1,
        "card_id": 123
    }
    response = client.post("/payment/create", json=payment_data)  # Envía datos como JSON
    assert response.status_code == 200  # Debería ser 200 si la creación es exitosa
    data = response.json()
    assert data["date"] == now.isoformat()
    assert data["user"] == "test_user"
    assert data["payment_quantity"] == 10.50
    assert data["payment_method"] == True
    assert data["vehicle_type"] == 1
    assert data["card_id"] == 123

def test_update_payment_existing(test_db):
    """Prueba la actualización de un pago existente."""
    now = datetime.datetime.now()
    # Primero, crea un pago para actualizar
    create_data = {
        "date": now.isoformat(),
        "user": "user_to_update",
        "payment_quantity": 20.00,
        "payment_method": False,
        "vehicle_type": 2,
        "card_id": 456
    }
    create_response = client.post("/payment/create", json=create_data)
    assert create_response.status_code == 200
    created_data = create_response.json()
    payment_id = created_data["id"]

    # Luego, actualiza el pago
    updated_data = {
        "id": payment_id,
        "date": now.isoformat(),
        "user": "updated_user",
        "payment_quantity": 30.00,
        "payment_method": True,
        "vehicle_type": 3,
        "card_id": 789
    }
    response = client.post(f"/payment/update", json=updated_data) # Usa POST para update
    assert response.status_code == 200
    data = response.json()
    assert data["user"] == "updated_user"
    assert data["payment_quantity"] == 30.00

def test_update_payment_not_found():
    """Prueba la actualización de un pago no existente."""
    now = datetime.datetime.now()
    updated_data = {
        "id": 9999,  # ID que no existe
        "date": now.isoformat(),
        "user": "nonexistent_user",
        "payment_quantity": 50.00,
        "payment_method": False,
        "vehicle_type": 1,
        "card_id": 123
    }
    response = client.post("/payment/update", json=updated_data) # Usa POST para update
    assert response.status_code == 404
    assert response.json()["detail"] == "Payment not found"

def test_delete_payment_existing(test_db):
    """Prueba la eliminación de un pago existente."""
    now = datetime.datetime.now()
    # Primero, crea un pago para eliminar
    create_data = {
        "date": now.isoformat(),
        "user": "user_to_delete",
        "payment_quantity": 15.75,
        "payment_method": True,
        "vehicle_type": 1,
        "card_id": 987
    }
    create_response = client.post("/payment/create", json=create_data)
    assert create_response.status_code == 200
    created_data = create_response.json()
    payment_id = created_data["id"]

    # Luego, elimina el pago
    response = client.post(f"/payment/delete", json={"id": payment_id}) # Usa POST para delete
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == f"Payment with id {payment_id} deleted successfully"

def test_delete_payment_not_found():
    """Prueba la eliminación de un pago no existente."""
    response = client.post("/payment/delete", json={"id": 9999}) # Usa POST para delete
    assert response.status_code == 404
    assert response.json()["detail"] == "Payment not found"

def test_index_create_form():
    """Prueba la ruta del formulario de creación."""
    response = client.get("/payment/crear")
    assert response.status_code == 200

def test_index_update_form():
    """Prueba la ruta del formulario de actualización."""
    response = client.get("/payment/actualizar")
    assert response.status_code == 200

def test_index_delete_form():
    """Prueba la ruta del formulario de eliminación."""
    response = client.get("/payment/eliminar")
    assert response.status_code == 200
