import pytest
import logging
from fastapi.testclient import TestClient
from backend.app.api.routes.shifts_cud_service import app
from backend.app.models.shift import Shift
from backend.app.logic.universal_controller_instance import universal_controller as controller
from backend.app.core.conf import headers

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("backend.app.api.routes.shifts_cud_service")

client = TestClient(app, raise_server_exceptions=False)

def test_crear_turno():
    turno_id = 9999
    turno_prueba = Shift(ID=turno_id, TipoTurno="Nocturno Test")
    existing_turno = controller.get_by_id(Shift, turno_id)
    if existing_turno:
        controller.delete(existing_turno)
    try:
        response = client.post("/shifts/create", data={"id": turno_id, "TipoTurno": "Nocturno Test"}, headers=headers)
        assert response.status_code == 200
        assert response.json()["message"] == "Turno creado exitosamente."
        logger.info("Test crear_turno ejecutado correctamente.")
    finally:
        controller.delete(turno_prueba)

def test_actualizar_turno():
    turno_id = 9999
    turno_prueba = Shift(ID=turno_id, TipoTurno="Original")
    existing_turno = controller.get_by_id(Shift, turno_id)
    if existing_turno:
        controller.delete(existing_turno)
    controller.add(turno_prueba)
    try:
        response = client.post("/shifts/update", data={"id": turno_id, "TipoTurno": "Vespertino Test"}, headers=headers)
        assert response.status_code == 200
        assert response.json()["message"] == "Turno actualizado exitosamente."
        turno_actualizado = controller.get_by_id(Shift, turno_id)
        assert turno_actualizado.TipoTurno == "Vespertino Test"
        logger.info(f"Test actualizar_turno ejecutado correctamente para ID={turno_id}.")
    finally:
        controller.delete(turno_prueba)

def test_actualizar_turno_no_existente():
    response = client.post("/shifts/update", data={"id": 88888, "TipoTurno": "No existe"}, headers=headers)
    assert response.status_code in (404, 500)
    logger.warning(
        f"Test actualizar_turno_no_existente ejecutado: status={response.status_code}, body={response.text}"
    )

def test_eliminar_turno():
    turno_id = 9999
    turno_prueba = Shift(ID=turno_id, TipoTurno="Eliminar Test")
    controller.add(turno_prueba)
    response = client.post("/shifts/delete", data={"id": turno_id}, headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Turno eliminado exitosamente."
    logger.info(f"Test eliminar_turno ejecutado correctamente para ID={turno_id}.")

def test_eliminar_turno_no_existente():
    response = client.post("/shifts/delete", data={"id": 88888}, headers=headers)
    assert response.status_code in (404, 500)
    logger.warning(
        f"Test eliminar_turno_no_existente ejecutado: status={response.status_code}, body={response.text}"
    )