import pytest
import logging
from fastapi.testclient import TestClient
from backend.app.api.routes.transport_unit_cud_service import app
from backend.app.models.transport import UnidadTransporte
from backend.app.logic.universal_controller_instance import universal_controller as controller

from backend.app.core.conf import headers

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("backend.app.api.routes.transport_unit_cud_service")

client = TestClient(app, raise_server_exceptions=False)

@pytest.fixture
def setup_and_teardown():
    """
    Fixture para configurar y limpiar los datos de prueba.
    """
    unidad = UnidadTransporte(Ubicacion="Depósito Central", Capacidad=50, IDRuta=1, IDTipo=2, ID="TEST_ID")
    existing = controller.get_by_id(UnidadTransporte, "TEST_ID")
    if existing:
        controller.delete(existing)
    controller.add(unidad)
    yield unidad
    controller.delete(unidad)

def test_crear_unidad_transporte():
    """
    Prueba para crear una unidad de transporte.
    """
    unidad = UnidadTransporte(Ubicacion="Depósito Secundario", Capacidad=30, IDRuta=1, IDTipo=2, ID="TEST_CREATE")
    try:
        response = client.post("/transport_units/create", data=unidad.to_dict(), headers=headers)
        assert response.status_code == 200
        assert response.json()["message"] == "Unidad de transporte creada exitosamente."
        logger.info("Test crear_unidad_transporte ejecutado correctamente.")
    finally:
        controller.delete(unidad)

def test_actualizar_unidad_transporte(setup_and_teardown):
    """
    Prueba para actualizar una unidad de transporte existente.
    """
    unidad = setup_and_teardown
    response = client.post(
        "/transport_units/update",
        data={
            "ID": unidad.ID,
            "Ubicacion": "Depósito Actualizado",
            "Capacidad": 60,
            "IDRuta": 1,
            "IDTipo": 2
        },
        headers=headers
    )
    print(response.text)
    assert response.status_code == 200
    assert response.json()["message"] == "Unidad de transporte actualizada exitosamente."
    logger.info(f"Test actualizar_unidad_transporte ejecutado correctamente para ID={unidad.ID}.")

def test_actualizar_unidad_transporte_no_existente():
    """
    Prueba para actualizar una unidad de transporte que no existe.
    """
    response = client.post(
        "/transport_units/update",
        data={
            "ID": "NO_EXISTE",
            "Ubicacion": "No existe",
            "Capacidad": 10,
            "IDRuta": 1,
            "IDTipo": 2
        },
        headers=headers
    )
    assert response.status_code in (404, 500)
    logger.warning(
        f"Test actualizar_unidad_transporte_no_existente ejecutado: status={response.status_code}, body={response.text}"
    )

def test_eliminar_unidad_transporte(setup_and_teardown):
    """
    Prueba para eliminar una unidad de transporte existente.
    """
    unidad = setup_and_teardown
    response = client.post("/transport_units/delete", data={"ID": unidad.ID}, headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Unidad de transporte eliminada exitosamente."
    logger.info(f"Test eliminar_unidad_transporte ejecutado correctamente para ID={unidad.ID}.")

def test_eliminar_unidad_transporte_no_existente():
    """
    Prueba para eliminar una unidad de transporte que no existe.
    """
    response = client.post("/transport_units/delete", data={"ID": "NO_EXISTE"}, headers=headers)
    assert response.status_code in (404, 500)
    logger.warning(
        f"Test eliminar_unidad_transporte_no_existente ejecutado: status={response.status_code}, body={response.text}"
    )