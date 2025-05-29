import pytest
import logging
from fastapi.testclient import TestClient
from backend.app.api.routes.maintainance_status_cud_service import app
from backend.app.models.maintainance_status import MaintainanceStatus
from backend.app.logic.universal_controller_instance import universal_controller as controller
from backend.app.core.conf import headers
from unittest.mock import patch

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("backend.app.api.routes.maintainance_status_cud_service")

client = TestClient(app)

@pytest.fixture
def setup_and_teardown():
    """
    Fixture para configurar y limpiar los datos de prueba.
    """
    estado_prueba = MaintainanceStatus(ID=9999, TipoEstado="Prueba")
    existing_estado = controller.get_by_id(MaintainanceStatus, estado_prueba.ID)
    if existing_estado:
        controller.delete(existing_estado)
    controller.add(estado_prueba)
    yield estado_prueba
    controller.delete(estado_prueba)

def test_crear_estado():
    """
    Prueba para crear un estado de mantenimiento.
    """
    estado_prueba = MaintainanceStatus(ID=9998, TipoEstado="Nuevo Estado")
    try:
        response = client.post("/maintainance_status/create", data={"ID": estado_prueba.ID, "TipoEstado": estado_prueba.TipoEstado}, headers=headers)
        assert response.status_code == 200
        assert response.json()["message"] == "Estado de mantenimiento creado exitosamente."
        logger.info("Test crear_estado ejecutado correctamente.")
    finally:
        controller.delete(estado_prueba)

def test_actualizar_estado(setup_and_teardown):
    """
    Prueba para actualizar un estado de mantenimiento existente.
    """
    estado_prueba = setup_and_teardown
    response = client.post("/maintainance_status/update", data={"id": estado_prueba.ID, "TipoEstado": "Estado Actualizado"}, headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Estado de mantenimiento actualizado exitosamente."
    logger.info(f"Test actualizar_estado ejecutado correctamente para ID={estado_prueba.ID}.")

    estado_actualizado = controller.get_by_id(MaintainanceStatus, estado_prueba.ID)
    assert estado_actualizado.TipoEstado == "Estado Actualizado"

def test_actualizar_estado_no_existente():
    """
    Prueba para actualizar un estado de mantenimiento que no existe.
    """
    with patch("backend.app.logic.universal_controller_instance.universal_controller.get_by_id", return_value=None):
        response = client.post("/maintainance_status/update", data={"id": 99999, "TipoEstado": "Error Actualizar"})
        
        # Verifica el código de estado
        assert response.status_code == 404, f"Error inesperado: {response.status_code}"
        
        # Verifica el mensaje de error en la respuesta
        response_json = response.json()
        assert "Estado de mantenimiento no encontrado" in response_json["detail"], "El mensaje de error no es el esperado."

def test_eliminar_estado(setup_and_teardown):
    """
    Prueba para eliminar un estado de mantenimiento existente.
    """
    estado_prueba = setup_and_teardown
    response = client.post("/maintainance_status/delete", data={"id": estado_prueba.ID}, headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Estado de mantenimiento eliminado exitosamente."
    logger.info(f"Test eliminar_estado ejecutado correctamente para ID={estado_prueba.ID}.")

    estado_eliminado = controller.get_by_id(MaintainanceStatus, estado_prueba.ID)
    assert estado_eliminado is None

def test_eliminar_estado_no_existente():
    """
    Prueba para eliminar un estado de mantenimiento que no existe.
    """
    with patch("backend.app.logic.universal_controller_instance.universal_controller.get_by_id", return_value=None):
        response = client.post("/maintainance_status/delete", data={"id": 99999})
        
        # Verifica el código de estado
        assert response.status_code == 404, f"Error inesperado: {response.status_code}"
        
        # Verifica el mensaje de error en la respuesta
        response_json = response.json()
        assert "Estado de mantenimiento no encontrado" in response_json["detail"], "El mensaje de error no es el esperado."

def test_error_al_crear_estado():
    """
    Prueba para simular un error al crear un estado de mantenimiento.
    """
    with patch("backend.app.logic.universal_controller_instance.universal_controller.add", side_effect=Exception("Simulated error")):
        response = client.post("/maintainance_status/create", data={"ID": 9999, "TipoEstado": "Error Estado"}, headers=headers)
        
        # Verifica el código de estado
        assert response.status_code == 400, f"Error inesperado: {response.status_code}"
        
        # Verifica si la respuesta contiene el mensaje esperado
        response_json = response.json()
        assert "Error al crear estado" in response_json["detail"], "El mensaje de error no es el esperado."

def test_error_al_actualizar_estado():
    """
    Prueba para simular un error al actualizar un estado de mantenimiento.
    """
    with patch("backend.app.logic.universal_controller_instance.universal_controller.update", side_effect=Exception("Simulated error")):
        response = client.post("/maintainance_status/update", data={"id": 9999, "TipoEstado": "Error Actualizar"}, headers=headers)
        
        # Verifica el código de estado
        assert response.status_code in (400, 404), f"Error inesperado: {response.status_code}"
        
        # Verifica si la respuesta contiene el mensaje esperado
        response_json = response.json()
        if response.status_code == 404:
            assert "Estado de mantenimiento no encontrado" in response_json["detail"], "El mensaje de error no es el esperado."
        else:
            assert "Error al actualizar estado" in response_json["detail"], "El mensaje de error no es el esperado."

def test_error_al_eliminar_estado():
    """
    Prueba para simular un error al eliminar un estado de mantenimiento.
    """
    with patch("backend.app.logic.universal_controller_instance.universal_controller.delete", side_effect=Exception("Simulated error")):
        response = client.post("/maintainance_status/delete", data={"id": 9999}, headers=headers)
        
        # Verifica el código de estado
        assert response.status_code in (400, 404), f"Error inesperado: {response.status_code}"
        
        # Verifica si la respuesta contiene el mensaje esperado
        response_json = response.json()
        if response.status_code == 404:
            assert "Estado de mantenimiento no encontrado" in response_json["detail"], "El mensaje de error no es el esperado."
        else:
            assert "Error al eliminar estado" in response_json["detail"], "El mensaje de error no es el esperado."