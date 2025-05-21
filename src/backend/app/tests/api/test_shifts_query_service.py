import pytest
import logging
from fastapi.testclient import TestClient
from backend.app.api.routes.shifts_query_service import app as shifts_router
from backend.app.logic.universal_controller_instance import universal_controller as controller
from backend.app.models.shift import Shift
from backend.app.core.conf import headers
from fastapi import FastAPI

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("backend.app.api.routes.shifts_query_service")

app_for_test = FastAPI()
app_for_test.include_router(shifts_router)
client = TestClient(app_for_test, raise_server_exceptions=False)

@pytest.fixture
def setup_and_teardown():
    turno_prueba = Shift(ID=99999, TipoTurno="Prueba")
    controller.add(turno_prueba)
    yield turno_prueba
    controller.delete(turno_prueba)

def test_listar_turnos(setup_and_teardown):
    response = client.get("/shifts/", headers=headers)
    assert response.status_code == 200
    assert "Prueba" in response.text
    logger.info("Test listar_turnos ejecutado correctamente.")

def test_detalle_turno_existente(setup_and_teardown):
    turno_prueba = setup_and_teardown
    response = client.get(f"/shifts/{turno_prueba.ID}", headers=headers)
    assert response.status_code == 200
    assert str(turno_prueba.ID) in response.text
    assert "Prueba" in response.text
    logger.info(f"Test detalle_turno_existente ejecutado correctamente para ID={turno_prueba.ID}.")

def test_detalle_turno_no_existente():
    response = client.get("/shifts/88888", headers=headers)
    assert response.status_code in (404, 500)
    logger.warning(
        f"Test detalle_turno_no_existente ejecutado: status={response.status_code}, body={response.text}"
    )