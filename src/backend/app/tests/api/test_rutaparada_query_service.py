import logging
from fastapi.testclient import TestClient
from backend.app.api.routes.rutaparada_query_service import app as rutaparada_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("backend.app.api.routes.rutaparada_query_service")

client = TestClient(rutaparada_router)

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
    Prueba para obtener el detalle de una relación Ruta-Parada existente (IDRuta=1, IDParada=1).
    """
    response = client.get("/ruta_parada/1")
    assert response.status_code == 200
    assert "DetalleRutaParada.html" in response.text or "Parada" in response.text
    logger.info("Test detalle_rutaparada_existente ejecutado correctamente para IDParada=1.")

