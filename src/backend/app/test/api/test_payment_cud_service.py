from fastapi.testclient import TestClient
from backend.app.api.routes.payment_cud_service import app as payments_router
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

def test_crear_pago():
    response = client.post("/payments/create", data={
        "id": 1,
        "user": "Juan",
        "payment_quantity": 100.0,
        "payment_method": True,
        "vehicle_type": 1,
        "card_id": 123
    })
    assert response.status_code == 200

def test_actualizar_pago():
    controller.add(Payment(id=1, user="Juan", payment_quantity=100.0, payment_method=True, vehicle_type=1, card_id=123))
    response = client.post("/payments/update", data={
        "id": 1,
        "user": "Juan",
        "payment_quantity": 150.0,
        "payment_method": False,
        "vehicle_type": 2,
        "card_id": 123
    })
    assert response.status_code == 200

def test_eliminar_pago():
    controller.add(Payment(id=1, user="Juan", payment_quantity=100.0, payment_method=True, vehicle_type=1, card_id=123))
    response = client.post("/payments/delete", data={"id": 1})
    assert response.status_code == 200

def test_controlador_eliminar_pago():
# Crear un pago de prueba directamente en el controlador
    controller.add(Payment(
        id=1,
        user="Juan",
        payment_quantity=100.0,
        payment_method=True,
        vehicle_type=1,
        card_id=123
    ))

    # Intentar eliminar el pago
    try:
        result = controller.delete(Payment(id=1))
        assert result is True
    except Exception as e:
        assert False, f"El controlador falló con el error: {e}"