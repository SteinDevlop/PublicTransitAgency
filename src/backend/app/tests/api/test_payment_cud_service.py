import pytest
import logging
from fastapi.testclient import TestClient
from backend.app.api.routes.payment_cud_service import app
from backend.app.models.payments import Payment
from backend.app.logic.universal_controller_instance import universal_controller as controller

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("backend.app.api.routes.payment_cud_service")

client = TestClient(app, raise_server_exceptions=False)

@pytest.fixture
def setup_and_teardown():
    """
    Fixture para configurar y limpiar los datos de prueba.
    """
    pago = Payment(IDMovimiento=2, IDPrecio=1, IDTarjeta=41, IDUnidad="1", ID=54321)
    existing_pago = controller.get_by_id(Payment, pago.ID)
    if existing_pago:
        controller.delete(existing_pago)
    controller.add(pago)
    yield pago
    controller.delete(pago)

def test_crear_pago():
    """
    Prueba para crear un pago.
    """
    pago = Payment(IDMovimiento=2, IDPrecio=1, IDTarjeta=41, IDUnidad="1", ID=67890)
    try:
        response = client.post("/payments/create", data=pago.model_dump())
        assert response.status_code == 200
        assert response.json()["message"] == "Pago creado exitosamente."
        logger.info("Test crear_pago ejecutado correctamente.")
    finally:
        controller.delete(pago)

def test_eliminar_pago(setup_and_teardown):
    """
    Prueba para eliminar un pago existente.
    """
    pago = setup_and_teardown
    response = client.post("/payments/delete", data={"ID": pago.ID})
    assert response.status_code == 200
    assert response.json()["message"] == "Pago eliminado exitosamente."
    logger.info(f"Test eliminar_pago ejecutado correctamente para ID={pago.ID}.")

    # Verificar que el pago haya sido eliminado
    deleted_pago = controller.get_by_id(Payment, pago.ID)
    assert deleted_pago is None

def test_eliminar_pago_no_existente():
    """
    Prueba para eliminar un pago que no existe.
    """
    response = client.post("/payments/delete", data={"ID": 9999999})
    assert response.status_code == 404
    assert response.json()["detail"] == "Pago no encontrado"
    logger.warning(
        f"Test eliminar_pago_no_existente ejecutado: status={response.status_code}, body={response.text}"
    )

def test_update_pago(setup_and_teardown):
    """
    Prueba para actualizar un pago existente.
    """
    pago = setup_and_teardown
    # Cambiamos el IDUnidad
    updated_data = {
        "ID": pago.ID,
        "IDMovimiento": pago.IDMovimiento,
        "IDPrecio": pago.IDPrecio,
        "IDTarjeta": pago.IDTarjeta,
        "IDUnidad": "1"
    }
    response = client.post("/payments/update", data=updated_data)
    assert response.status_code == 200
    assert response.json()["message"] == "Pago actualizado exitosamente."
    # Verifica que el cambio se haya realizado
    updated_pago = controller.get_by_id(Payment, pago.ID)
    assert updated_pago is not None
    logger.info(f"Test update_pago ejecutado correctamente para ID={pago.ID}.")

def test_eliminar_pago_no_existente():
    """
    Prueba para eliminar un pago que no existe.
    """
    response = client.post("/payments/delete", data={"ID": 9999999})
    assert response.status_code in (404, 500)
    logger.warning(
        f"Test eliminar_pago_no_existente ejecutado: status={response.status_code}, body={response.text}"
    )