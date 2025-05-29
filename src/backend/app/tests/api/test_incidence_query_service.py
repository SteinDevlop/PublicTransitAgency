import pytest
import logging
from fastapi.testclient import TestClient
from backend.app.api.routes.incidence_query_service import app
from backend.app.models.incidence import Incidence
from backend.app.logic.universal_controller_instance import universal_controller as controller
from backend.app.core.conf import headers
from unittest.mock import patch

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

def test_listar_incidencias_formato_json(setup_and_teardown):
    """
    Prueba para validar que el listado de incidencias se devuelve en formato JSON.
    """
    response = client.get("/incidences/", headers=headers)
    assert response.status_code == 200, f"Error inesperado: {response.status_code}"
    assert isinstance(response.json(), list), "La respuesta no es una lista."
    assert len(response.json()) > 0, "No se encontraron incidencias en el listado."
    logger.info("Test listar_incidencias_formato_json ejecutado correctamente.")

def test_error_al_eliminar_estado():
    """
    Prueba para simular un error al eliminar un estado de mantenimiento.
    """
    with patch("backend.app.logic.universal_controller_instance.universal_controller.delete", side_effect=Exception("Simulated error")):
        response = client.post("/maintainance_status/delete", data={"id": 9999}, headers=headers)
        
        # Verifica el código de estado
        assert response.status_code in (400, 404), f"Error inesperado: {response.status_code}"
        
        # Verifica si la respuesta es JSON antes de intentar decodificarla
        try:
            response_json = response.json()
            assert "Error al eliminar estado" in response_json["detail"], "El mensaje de error no es el esperado."
        except Exception:
            assert response.text == "Not Found", "El mensaje de error no coincide con 'Not Found'."