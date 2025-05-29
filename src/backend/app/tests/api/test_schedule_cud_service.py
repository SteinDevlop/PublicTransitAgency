import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from backend.app.api.routes.schedule_cud_service import app
from backend.app.models.schedule import Schedule
from backend.app.logic.universal_controller_instance import universal_controller as controller

from backend.app.core.conf import headers

client = TestClient(app)

@pytest.fixture
def setup_and_teardown():
    """
    Fixture para configurar y limpiar los datos de prueba.
    """
    horario = Schedule(ID=9999, Llegada="08:00", Salida="18:00")
    controller.add(horario)
    yield horario
    controller.delete(horario)

def test_crear_horario():
    """
    Prueba para crear un nuevo horario.
    """
    horario = Schedule(ID=9998, Llegada="09:00", Salida="19:00")
    try:
        response = client.post("/schedules/create", data=horario.to_dict(), headers=headers)
        assert response.status_code == 200
        assert response.json()["message"] == "Horario creado exitosamente."
    finally:
        controller.delete(horario)

def test_actualizar_horario(setup_and_teardown):
    """
    Prueba para actualizar un horario existente.
    """
    horario = setup_and_teardown
    response = client.post(
        "/schedules/update",
        data={"ID": horario.ID, "Llegada": "10:00", "Salida": "20:00"},
        headers=headers
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Horario actualizado exitosamente."

def test_eliminar_horario(setup_and_teardown):
    """
    Prueba para eliminar un horario existente.
    """
    horario = setup_and_teardown
    response = client.post("/schedules/delete", data={"ID": horario.ID}, headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Horario eliminado exitosamente."




def test_eliminar_horario_no_existente():
    """
    Prueba para manejar un error al eliminar un horario inexistente.
    """
    response = client.post("/schedules/delete", data={"ID": 999999}, headers=headers)
    assert response.status_code == 404
    assert "Horario no encontrado" in response.json()["detail"]

def test_error_al_crear_horario():
    """
    Prueba para simular un error al crear un horario.
    """
    with patch("backend.app.logic.universal_controller_instance.universal_controller.add", side_effect=Exception("Simulated error")):
        response = client.post("/schedules/create", data={"ID": 9999, "Llegada": "08:00", "Salida": "18:00"}, headers=headers)
        assert response.status_code == 400
        assert "Error al crear el horario" in response.json()["detail"]

def test_error_al_actualizar_horario():
    """
    Prueba para simular un error al actualizar un horario.
    """
    with patch("backend.app.logic.universal_controller_instance.universal_controller.update", side_effect=Exception("Simulated error")):
        response = client.post("/schedules/update", data={"ID": 9999, "Llegada": "09:00", "Salida": "19:00"}, headers=headers)
        assert response.status_code == 400
        assert "Error al actualizar el horario" in response.json()["detail"]

def test_error_al_eliminar_horario():
    """
    Prueba para simular un error al eliminar un horario.
    """
    with patch("backend.app.logic.universal_controller_instance.universal_controller.delete", side_effect=Exception("Simulated error")):
        response = client.post("/schedules/delete", data={"ID": 9999}, headers=headers)
        assert response.status_code in (400, 404)
        assert "Horario no encontrado" in response.json()["detail"]