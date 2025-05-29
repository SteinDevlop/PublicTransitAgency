import pytest
import logging
from fastapi.testclient import TestClient
from backend.app.api.routes.transport_unit_query_service import app
from backend.app.models.transport import UnidadTransporte
from backend.app.logic.universal_controller_instance import universal_controller as controller

from backend.app.core.conf import headers

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("backend.app.api.routes.transport_unit_query_service")

client = TestClient(app, raise_server_exceptions=False)

@pytest.fixture
def setup_and_teardown():
    """
    Fixture para configurar y limpiar los datos de prueba.
    """
    unidad = UnidadTransporte(Ubicacion="Depósito Central", Capacidad=50, IDRuta=1, IDTipo=2, ID="EMPTY")
    controller.add(unidad)
    yield unidad
    controller.delete(unidad)

def test_listar_unidades_transporte(setup_and_teardown):
    """
    Prueba para listar todas las unidades de transporte.
    """
    response = client.get("/transport_units/", headers=headers)
    assert response.status_code == 200
    assert "Depósito Central" in response.text
    logger.info("Test listar_unidades_transporte ejecutado correctamente.")

def test_detalle_unidad_transporte_existente(setup_and_teardown):
    """
    Prueba para obtener el detalle de una unidad de transporte existente.
    """
    unidad = setup_and_teardown
    response = client.get(f"/transport_units/{unidad.ID}", headers=headers)
    assert response.status_code == 200
    assert "Depósito Central" in response.text
    logger.info(f"Test detalle_unidad_transporte_existente ejecutado correctamente para ID={unidad.ID}.")

def test_detalle_unidad_transporte_no_existente():
    """
    Prueba para obtener el detalle de una unidad de transporte que no existe.
    """
    response = client.get("/transport_units/NO_EXISTE", headers=headers)
    assert response.status_code in (404, 500)
    logger.warning(
        f"Test detalle_unidad_transporte_no_existente ejecutado: status={response.status_code}, body={response.text}"
    )