import logging
from fastapi.testclient import TestClient
from backend.app.api.routes.rutaparada_cud_service import app as rutaparada_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("backend.app.api.routes.rutaparada_cud_service")

client = TestClient(rutaparada_router, raise_server_exceptions=False)

def test_crear_rutaparada():
    """
    Prueba para crear una relación Ruta-Parada.
    """
    data = {"IDRuta": 9, "IDParada": 30}
    response = client.post("/rutaparada/create", data=data)
    assert response.status_code == 200
    assert "creada exitosamente" in response.json()["message"]
    logger.info("Test crear_rutaparada ejecutado correctamente.")

def test_eliminar_rutaparada():
    """
    Prueba para eliminar una relación Ruta-Parada existente.
    """
    data = {"IDRuta": 9, "IDParada": 30}
    response = client.post("/rutaparada/delete", data=data)
    assert response.status_code == 200
    assert "eliminada exitosamente" in response.json()["message"]
    logger.info("Test eliminar_rutaparada ejecutado correctamente.")


def test_actualizar_rutaparada():
    """
    Prueba para actualizar una relación Ruta-Parada (cambiar ambos IDs).
    """
    # Primero crea la relación original
    data_original = {"IDRuta": 9, "IDParada": 30}
    client.post("/rutaparada/create", data=data_original)
    # Actualiza la relación
    data_update = {
        "IDRuta": 9,
        "IDParada": 30,
        "nuevo_IDRuta": 10,
        "nuevo_IDParada": 4
    }
    response = client.post("/rutaparada/update", data=data_update)
    assert response.status_code == 200
    assert "actualizada exitosamente" in response.json()["message"]
    logger.info("Test actualizar_rutaparada ejecutado correctamente.")
    # Limpieza: elimina la relación actualizada
    client.post("/rutaparada/delete", data={"IDRuta": 10, "IDParada": 4})

