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
    logger.info("Test listar_rutas_con_paradas ejecutado correctamente.")

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
