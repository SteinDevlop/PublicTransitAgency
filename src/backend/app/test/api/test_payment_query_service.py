from fastapi import FastAPI
from fastapi.testclient import TestClient
from backend.app.api.routes.payment_query_service import app as payment_router
from backend.app.logic.universal_controller_sql import UniversalController
from backend.app.models.payments import PaymentCreate

def setup_function():
    uc = UniversalController()
    uc.clear_tables()
    # Crear algunos pagos de prueba
    uc.add(PaymentCreate(date="2025-04-30T20:00:00", user="user1", payment_quantity=5.00, payment_method=True, vehicle_type=1, card_id=101))
    uc.add(PaymentCreate(date="2025-04-30T20:15:00", user="user2", payment_quantity=12.50, payment_method=False, vehicle_type=2, card_id=102))

def teardown_function():
    UniversalController().clear_tables()

app_for_test = FastAPI()
app_for_test.include_router(payment_router)
client = TestClient(app_for_test)

def test_get_all_payments():
    response = client.get("/payments/all")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["user"] == "user1"
    assert data[1]["payment_quantity"] == 12.50

def test_get_payment_by_id_existing():
    response = client.get("/payments/1") # Assuming the first created has ID 1
    assert response.status_code == 200
    data = response.json()
    assert data["user"] == "user1"
    assert data["vehicle_type"] == 1

def test_get_payment_by_id_not_found():
    """Prueba que la ruta '/payments/{payment_id}' devuelve un error 404 si el pago no existe."""
    response = client.get("/payments/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Payment not found"

def test_list_payments_page():
    response = client.get("/payments/listar")
    assert response.status_code == 200
    assert "Listado de Pagos" in response.text # Verifica el título de la página

def test_payment_detail_page_existing():
    response = client.get("/payments/detalles/1") # Assuming the first created has ID 1
    assert response.status_code == 200
    assert "Detalle del Pago" in response.text # Verifica el título de la página
    assert "user1" in response.text

def test_payment_detail_page_not_found():
    response = client.get("/payments/detalles/999")
    assert response.status_code == 200 # Aunque no encuentre, la página podría renderizar sin datos
    assert "Detalle del Pago" in response.text
    assert "None" in response.text # O algún indicador de que no se encontró