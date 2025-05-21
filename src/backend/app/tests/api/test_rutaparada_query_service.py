import logging
from fastapi.testclient import TestClient
from backend.app.api.routes.rutaparada_query_service import app as rutaparada_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("backend.app.api.routes.rutaparada_query_service")

client = TestClient(rutaparada_router, raise_server_exceptions=False)

def test_listar_rutaparada():
    """
    Prueba para listar todas las relaciones Ruta-Parada.
    """
    response = client.get("/ruta_parada/")
    assert response.status_code == 200
    assert "ListarRutaParada.html" in response.text or "Lista de Rutas y Paradas" in response.text
    logger.info("Test listar_rutaparada ejecutado correctamente.")

def test_detalle_rutaparada_existente():
    """
    Prueba para obtener el detalle de una relación Ruta-Parada existente (IDParada=1).
    """
    response = client.get("/ruta_parada/1")
    assert response.status_code == 200
    assert "DetalleRutaParada.html" in response.text or "Parada" in response.text
    logger.info("Test detalle_rutaparada_existente ejecutado correctamente para IDParada=1.")

def test_detalle_rutaparada_no_existente():
    """
    Prueba para obtener el detalle de una relación Ruta-Parada inexistente (IDParada=99999).
    """
    response = client.get("/ruta_parada/99999")
    assert response.status_code in (404, 500)
    logger.warning(
        f"Test detalle_rutaparada_no_existente ejecutado: status={response.status_code}, body={response.text}"
    )