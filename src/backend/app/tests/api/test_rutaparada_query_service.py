import logging
from fastapi.testclient import TestClient
from backend.app.api.routes.rutaparada_query_service import app as rutaparada_router
from unittest.mock import patch

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("backend.app.api.routes.rutaparada_query_service")

client = TestClient(rutaparada_router, raise_server_exceptions=False)

def test_listar_rutas_con_paradas():
    """
    Prueba para listar todas las rutas junto con sus paradas.
    """
    response = client.get("/ruta_parada/")
    assert response.status_code in (200, 404), f"Error inesperado: {response.status_code}"
    if response.status_code == 200:
        assert "data" in response.json(), "La respuesta no contiene el campo 'data'."
        assert isinstance(response.json()["data"], list), "El campo 'data' no es una lista."
    elif response.status_code == 404:
        assert "No se encontraron registros." in response.json()["detail"]
    logger.info("Test listar_rutas_con_paradas ejecutado correctamente.")

def test_listar_rutas_con_paradas_no_registros():
    """
    Prueba para el caso en que no hay registros de ruta-parada (404).
    """
    with patch("backend.app.logic.universal_controller_instance.universal_controller.read_all", return_value=[]):
        response = client.get("/ruta_parada/")
        assert response.status_code == 404
        assert "No se encontraron registros." in response.json()["detail"]
        logger.warning("Test listar_rutas_con_paradas_no_registros ejecutado correctamente.")

def test_buscar_por_id_parada_existente():
    """
    Prueba para buscar rutas asociadas a una parada existente (IDParada=30).
    """
    response = client.get("/ruta_parada/30")
    assert response.status_code == 200, f"Error inesperado: {response.status_code}"
    assert "data" in response.json(), "La respuesta no contiene el campo 'data'."
    assert isinstance(response.json()["data"], list), "El campo 'data' no es una lista."
    assert len(response.json()["data"]) > 0, "No se encontraron registros para la parada especificada."
    logger.info("Test buscar_por_id_parada_existente ejecutado correctamente para IDParada=30.")

def test_buscar_por_id_parada_no_existente():
    """
    Prueba para buscar rutas asociadas a una parada inexistente (IDParada=99999).
    """
    response = client.get("/ruta_parada/99999")
    assert response.status_code == 404, f"Error inesperado: {response.status_code}"
    assert "No se encontraron registros para la parada especificada." in response.json()["detail"], "El mensaje de error no es el esperado."
    logger.warning("Test buscar_por_id_parada_no_existente ejecutado correctamente para IDParada=99999.")

def test_listar_rutas_con_paradas_error_interno():
    """
    Prueba para manejar un error interno al listar las relaciones Ruta-Parada.
    """
    with patch("backend.app.logic.universal_controller_instance.universal_controller.read_all", side_effect=Exception("Simulated error")):
        response = client.get("/ruta_parada/")
        assert response.status_code == 500, f"Error inesperado: {response.status_code}"
        response_json = response.json()
        assert "Error interno al listar las relaciones Ruta-Parada." in response_json.get("detail", ""), "El mensaje de error no es el esperado."
        logger.error("Test listar_rutas_con_paradas_error_interno ejecutado correctamente.")

def test_buscar_por_id_parada_error_interno():
    """
    Prueba para manejar un error interno al obtener el detalle de la relación Ruta-Parada.
    """
    with patch("backend.app.logic.universal_controller_instance.universal_controller.get_by_id", side_effect=Exception("Simulated error")):
        response = client.get("/ruta_parada/99999")
        assert response.status_code == 500, f"Error inesperado: {response.status_code}"
        response_json = response.json()
        assert "Error interno al obtener el detalle de la relación Ruta-Parada." in response_json.get("detail", ""), "El mensaje de error no es el esperado."
        logger.error("Test buscar_por_id_parada_error_interno ejecutado correctamente.")
