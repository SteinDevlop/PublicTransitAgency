import logging
from fastapi.testclient import TestClient
from backend.app.api.routes.rutaparada_cud_service import app as rutaparada_router
from unittest.mock import patch
from backend.app.core.conf import headers

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("backend.app.api.routes.rutaparada_cud_service")

client = TestClient(rutaparada_router, raise_server_exceptions=False)

def test_crear_rutaparada():
    """
    Prueba para crear una relación Ruta-Parada.
    """
    data = {"IDRuta": 9, "IDParada": 30}
    response = client.post("/rutaparada/create", data=data, headers=headers)
    assert response.status_code == 200
    assert "creada exitosamente" in response.json()["message"]
    logger.info("Test crear_rutaparada ejecutado correctamente.")

def test_eliminar_rutaparada():
    """
    Prueba para eliminar una relación Ruta-Parada existente.
    """
    data = {"IDRuta": 9, "IDParada": 30}
    response = client.post("/rutaparada/delete", data=data, headers=headers)
    assert response.status_code == 200
    assert "eliminada exitosamente" in response.json()["message"]
    logger.info("Test eliminar_rutaparada ejecutado correctamente.")


def test_actualizar_rutaparada():
    """
    Prueba para actualizar una relación Ruta-Parada (cambiar ambos IDs).
    """
    # Primero crea la relación original
    data_original = {"IDRuta": 9, "IDParada": 30}
    client.post("/rutaparada/create", data=data_original, headers=headers)
    # Actualiza la relación
    data_update = {
        "IDRuta": 9,
        "IDParada": 30,
        "nuevo_IDRuta": 1,
        "nuevo_IDParada": 30
    }
    response = client.post("/rutaparada/update", data=data_update, headers=headers)
    assert response.status_code == 200
    assert "actualizada exitosamente" in response.json()["message"]
    logger.info("Test actualizar_rutaparada ejecutado correctamente.")
    # Limpieza: elimina la relación actualizada
    client.post("/rutaparada/delete", data={"IDRuta": 1, "IDParada": 30}, headers=headers)

def test_actualizar_rutaparada_no_existente():
    """
    Prueba para intentar actualizar una relación Ruta-Parada que no existe.
    """
    data_update = {
        "IDRuta": 99,  # IDs que no existen
        "IDParada": 99,
        "nuevo_IDRuta": 100,
        "nuevo_IDParada": 101
    }
    response = client.post("/rutaparada/update", data=data_update, headers=headers)
    assert response.status_code in (404, 500)  # Verifica que el código de estado sea 404 o 500
    logger.info("Test actualizar_rutaparada_no_existente ejecutado correctamente.")

def test_eliminar_rutaparada_no_existente():
    """
    Prueba para intentar eliminar una relación Ruta-Parada que no existe.
    """
    data = {"IDRuta": 99, "IDParada": 99}  # IDs que no existen
    response = client.post("/rutaparada/delete", data=data, headers=headers)
    assert response.status_code in (404, 500)  # Verifica que el código de estado sea 404 o 500
    logger.info("Test eliminar_rutaparada_no_existente ejecutado correctamente.")

def test_crear_rutaparada_ya_existente():
    """
    Prueba para intentar crear una relación Ruta-Parada que ya existe.
    """
    data = {"IDRuta": 9, "IDParada": 30}
    client.post("/rutaparada/create", data=data, headers=headers)
    response = client.post("/rutaparada/create", data=data, headers=headers)
    assert response.status_code == 409, f"Error inesperado: {response.status_code}"
    assert "La relación Ruta-Parada ya existe." in response.json()["detail"], "El mensaje de error no es el esperado."

def test_crear_rutaparada_error_interno():
    """
    Prueba para manejar un error interno al crear una relación Ruta-Parada.
    """
    with patch("backend.app.logic.universal_controller_instance.universal_controller.add", side_effect=Exception("Simulated error")):
        data = {"IDRuta": 9, "IDParada": 30}
        response = client.post("/rutaparada/create", data=data, headers=headers)
        
        # Verifica el código de estado
        if response.status_code == 409:
            assert "La relación Ruta-Parada ya existe." in response.json()["detail"], "El mensaje de error no es el esperado."
        elif response.status_code == 500:
            assert "Error interno al crear la relación Ruta-Parada" in response.json()["detail"], "El mensaje de error no es el esperado."
        else:
            assert False, f"Error inesperado: {response.status_code}"

def test_actualizar_rutaparada_error_interno():
    """
    Prueba para manejar un error interno al actualizar una relación Ruta-Parada.
    """
    with patch("backend.app.logic.universal_controller_instance.universal_controller.update", side_effect=Exception("Simulated error")):
        data_update = {"IDRuta": 9, "IDParada": 30, "nuevo_IDRuta": 10, "nuevo_IDParada": 4}
        response = client.post("/rutaparada/update", data=data_update, headers=headers)
        assert response.status_code == 500, f"Error inesperado: {response.status_code}"
        assert "Error interno al actualizar la relación Ruta-Parada" in response.json()["detail"], "El mensaje de error no es el esperado."

def test_eliminar_rutaparada_error_interno():
    """
    Prueba para manejar un error interno al eliminar una relación Ruta-Parada.
    """
    with patch("backend.app.logic.universal_controller_instance.universal_controller.delete", side_effect=Exception("Simulated error")):
        data = {"IDRuta": 9, "IDParada": 30}
        response = client.post("/rutaparada/delete", data=data, headers=headers)
        
        # Verifica el código de estado
        if response.status_code == 200:
            assert "Relación Ruta-Parada eliminada exitosamente." in response.json()["message"], "El mensaje de éxito no es el esperado."
        elif response.status_code == 500:
            assert "Error interno al eliminar la relación Ruta-Parada" in response.json()["detail"], "El mensaje de error no es el esperado."
        else:
            assert False, f"Error inesperado: {response.status_code}"