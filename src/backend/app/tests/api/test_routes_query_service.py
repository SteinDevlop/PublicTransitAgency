import pytest
import logging
from fastapi.testclient import TestClient
from backend.app.api.routes.routes_query_service import app
from backend.app.models.routes import Ruta
from backend.app.logic.universal_controller_instance import universal_controller as controller
from unittest.mock import patch

from backend.app.core.conf import headers

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("backend.app.api.routes.routes_query_service")

client = TestClient(app, raise_server_exceptions=False)

@pytest.fixture
def setup_and_teardown():
    """
    Configura y limpia datos de prueba para las rutas.
    """
    ruta = Ruta(ID=9999, IDHorario=1, Nombre="Ruta de Prueba")
    controller.add(ruta)
    yield ruta
    controller.delete(ruta)

def test_listar_rutas(setup_and_teardown):
    """
    Prueba para listar todas las rutas.
    """
    response = client.get("/routes/", headers=headers)
    assert response.status_code == 200, f"Error inesperado: {response.status_code}"
    rutas = response.json()
    assert isinstance(rutas, list), "La respuesta debe ser una lista."
    assert any(r.get("Nombre") == "Ruta de Prueba" for r in rutas), "No se encontró la ruta de prueba en la lista."
    logger.info("Test listar_rutas ejecutado correctamente.")

def test_detalle_ruta_existente(setup_and_teardown):
    """
    Prueba para obtener el detalle de una ruta existente.
    """
    ruta = setup_and_teardown
    response = client.get(f"/routes/{ruta.ID}", headers=headers)
    assert response.status_code == 200, f"Error inesperado: {response.status_code}"
    assert "data" in response.json(), "La respuesta no contiene el campo 'data'."
    assert response.json()["data"]["ID"] == ruta.ID, "El ID de la ruta no coincide."
    assert response.json()["data"]["Nombre"] == "Ruta de Prueba", "El nombre de la ruta no coincide."
    logger.info(f"Test detalle_ruta_existente ejecutado correctamente para ID={ruta.ID}.")

def test_detalle_ruta_no_existente():
    """
    Prueba para obtener el detalle de una ruta inexistente.
    """
    response = client.get("/routes/99999", headers=headers)
    assert response.status_code == 404, f"Error inesperado: {response.status_code}"
    assert "detail" in response.json(), "La respuesta no contiene el campo 'detail'."
    assert "No se encontró la ruta especificada." in response.json()["detail"], "El mensaje de error no es el esperado."
    logger.warning(
        f"Test detalle_ruta_no_existente ejecutado correctamente: status={response.status_code}, body={response.text}"
    )

def test_detalle_ruta_error_interno():
    """
    Prueba para manejar un error interno al consultar una ruta.
    """
    with patch("backend.app.logic.universal_controller_instance.universal_controller.get_by_id", side_effect=Exception("Error interno")):
        response = client.get("/routes/99999")
        
        # Verifica el código de estado
        assert response.status_code == 500, f"Error inesperado: {response.status_code}"
        
        # Verifica el mensaje de error en la respuesta
        response_json = response.json()
        assert "Error interno al consultar ruta" in response_json["detail"], "El mensaje de error no es el esperado."