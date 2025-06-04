import pytest
import logging
from fastapi.testclient import TestClient
from backend.app.api.routes.payment_query_service import app
from backend.app.models.payments import Payment
from backend.app.logic.universal_controller_instance import universal_controller as controller
from backend.app.core.conf import headers

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("backend.app.api.routes.payment_query_service")

client = TestClient(app, raise_server_exceptions=False)

@pytest.fixture
def setup_and_teardown():
    """
    Fixture para configurar y limpiar los datos de prueba.
    """
    pago = Payment(IDMovimiento=2, IDPrecio=1, IDTarjeta=42, IDUnidad="1", ID=12345)
    existing_pago = controller.get_by_id(Payment, pago.ID)
    if existing_pago:
        controller.delete(existing_pago)
    controller.add(pago)
    yield pago
    controller.delete(pago)

def test_listar_pagos(setup_and_teardown):
    """
    Prueba para listar todos los pagos.
    """
    response = client.get("/payments/", headers=headers)
    assert response.status_code == 200
    assert "Pagos listados exitosamente." in response.json()["message"]
    logger.info("Test listar_pagos ejecutado correctamente.")

def test_listar_pagos_error():
    """
    Prueba para manejar un error al listar pagos.
    """
    controller.read_all = lambda model: (_ for _ in ()).throw(Exception("Simulated error"))
    response = client.get("/payments/", headers=headers)
    assert response.status_code == 500
    assert response.json()["detail"] == "Error al listar pagos."
    logger.info("Test listar_pagos_error ejecutado correctamente.")

def test_detalle_pago_existente(setup_and_teardown):
    """
    Prueba para obtener el detalle de un pago existente.
    """
    pago = setup_and_teardown
    response = client.get(f"/payments/{pago.ID}", headers=headers)
    assert response.status_code == 200
    assert "Detalle de pago consultado exitosamente." in response.json()["message"]
    logger.info(f"Test detalle_pago_existente ejecutado correctamente para ID={pago.ID}.")

def test_detalle_pago_no_existente():
    """
    Prueba para manejar un error al consultar el detalle de un pago inexistente.
    """
    response = client.get("/payments/99999", headers=headers)  # ID que no existe
    assert response.status_code in (404, 500)
    assert "Pago no encontrado." in response.json()["detail"] or "Error al consultar detalle de pago." in response.json()["detail"]
    logger.info("Test detalle_pago_no_existente ejecutado correctamente.")

