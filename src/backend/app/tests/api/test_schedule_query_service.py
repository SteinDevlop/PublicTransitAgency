import pytest
import logging
from fastapi.testclient import TestClient
from backend.app.api.routes.schedule_query_service import app
from backend.app.models.schedule import Schedule
from backend.app.logic.universal_controller_instance import universal_controller as controller
from backend.app.core.conf import headers
from unittest.mock import patch

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("backend.app.api.routes.schedule_query_service")

client = TestClient(app)

@pytest.fixture
def setup_and_teardown():
    """
    Fixture para configurar y limpiar los datos de prueba.
    """
    # Usar strings en formato HH:MM
    schedule = Schedule(ID=9999, Llegada="08:00", Salida="17:00")
    # Asegurarse de que el horario no exista antes de crearlo
    existing_schedule = controller.get_by_id(Schedule, schedule.ID)
    if existing_schedule:
        controller.delete(existing_schedule)

    # Crear el horario de prueba
    controller.add(schedule)
    yield schedule

    # Eliminar el horario de prueba
    controller.delete(schedule)

def test_listar_horarios(setup_and_teardown):
    """
    Prueba para listar todos los horarios.
    """
    response = client.get("/schedules/", headers=headers)
    assert response.status_code == 200
    assert "Horarios listados exitosamente." in response.json()["message"]
    assert isinstance(response.json()["data"], list)
    assert len(response.json()["data"]) > 0
    logger.info("Test listar_horarios ejecutado correctamente. Se listaron %d horarios.", len(response.json()["data"]))

def test_listar_horarios_error():
    """
    Prueba para manejar un error al listar los horarios.
    """
    controller.read_all = lambda model: (_ for _ in ()).throw(Exception("Simulated error"))
    response = client.get("/schedules/", headers=headers)
    assert response.status_code == 500
    assert "Error al listar los horarios" in response.json()["detail"]
    logger.error("Test listar_horarios_error ejecutado correctamente. Error simulado al listar horarios.")

def test_detalle_horario_existente(setup_and_teardown):
    """
    Prueba para obtener el detalle de un horario existente.
    """
    schedule = setup_and_teardown
    response = client.get(f"/schedules/{schedule.ID}", headers=headers)
    assert response.status_code == 200
    assert "Detalle horario consultado exitosamente." in response.json()["message"]
    assert response.json()["data"]["ID"] == schedule.ID
    logger.info("Test detalle_horario_existente ejecutado correctamente para ID=%d.", schedule.ID)

def test_detalle_horario_no_existente():
    """
    Prueba para manejar un error al consultar el detalle de un horario inexistente.
    """
    response = client.get("/schedules/99999", headers=headers)  # ID que no existe
    assert response.status_code == 404
    assert "Horario no encontrado" in response.json()["detail"]
    logger.warning("Test detalle_horario_no_existente ejecutado correctamente. ID=99999 no encontrado.")

def test_detalle_horario_error_interno():
    """
    Prueba para manejar un error interno al consultar el detalle de un horario.
    """
    with patch("backend.app.logic.universal_controller_instance.universal_controller.get_by_id", side_effect=Exception("Simulated error")):
        response = client.get("/schedules/99999", headers=headers)
        
        # Verifica el código de estado
        assert response.status_code == 500, f"Error inesperado: {response.status_code}"
        
        # Verifica el mensaje de error en la respuesta
        response_json = response.json()
        assert "Error al consultar detalle de horario" in response_json["detail"], "El mensaje de error no es el esperado."
        logger.error("Test detalle_horario_error_interno ejecutado correctamente.")

