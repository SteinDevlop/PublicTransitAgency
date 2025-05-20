import pytest
import logging
from fastapi.testclient import TestClient
from backend.app.api.routes.incidence_query_service import app
from backend.app.models.incidence import Incidence
from backend.app.logic.universal_controller_instance import universal_controller as controller
from backend.app.core.conf import headers

# Configuración de logging para capturar logs de los endpoints
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("backend.app.api.routes.incidence_query_service")

client = TestClient(app)

@pytest.fixture
def setup_and_teardown():
    """
    Fixture para configurar y limpiar los datos de prueba.
    """
    incidencia = Incidence(ID=9998, IDTicket=1, Descripcion="Nueva incidencia", Tipo="Advertencia", IDUnidad="1")
    controller.add(incidencia)
    yield incidencia
    controller.delete(incidencia)

def test_listar_incidencias(setup_and_teardown):
    """
    Prueba para listar todas las incidencias.
    """
    response = client.get("/incidences/", headers=headers)
    assert response.status_code == 200
    logger.info("Test listar_incidencias ejecutado correctamente.")

def test_detalle_incidencia_existente(setup_and_teardown):
    """
    Prueba para obtener el detalle de una incidencia existente.
    """
    incidencia = setup_and_teardown
    response = client.get(f"/incidences/{incidencia.ID}", headers=headers)
    assert response.status_code == 200
    logger.info(f"Test detalle_incidencia_existente ejecutado correctamente para ID={incidencia.ID}.")