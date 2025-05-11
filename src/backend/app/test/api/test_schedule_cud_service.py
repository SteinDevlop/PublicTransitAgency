import pytest
from fastapi.testclient import TestClient
from backend.app.api.routes.schedule_cud_service import app
from backend.app.models.schedule import Schedule
from backend.app.logic.universal_controller_sqlserver import UniversalController
from backend.app.core.conf import headers

client = TestClient(app)
controller = UniversalController()

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
        data={"id": horario.ID, "Llegada": "10:00", "Salida": "20:00"},
        headers=headers
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Horario actualizado exitosamente."

def test_eliminar_horario(setup_and_teardown):
    """
    Prueba para eliminar un horario existente.
    """
    horario = setup_and_teardown
    response = client.post("/schedules/delete", data={"id": horario.ID}, headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Horario eliminado exitosamente."


