import pytest
import logging
from fastapi.testclient import TestClient
from backend.app.api.routes.maintainance_status_query_service import app
from backend.app.models.maintainance_status import MaintainanceStatus
from backend.app.logic.universal_controller_instance import universal_controller as controller
from backend.app.core.conf import headers

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("backend.app.api.routes.maintainance_status_query_service")

client = TestClient(app, raise_server_exceptions=False)

@pytest.fixture
def setup_and_teardown():
    estado = MaintainanceStatus(ID=9999, TipoEstado="ConsultaTest")
    existing = controller.get_by_id(MaintainanceStatus, estado.ID)
    if existing:
        controller.delete(existing)
    controller.add(estado)
    yield estado
    controller.delete(estado)

def test_listar_estados(setup_and_teardown):
    response = client.get("/maintainance_status/", headers=headers)
    assert response.status_code == 200
    logger.info("Test listar_estados ejecutado correctamente.")

def test_detalle_estado_existente(setup_and_teardown):
    estado = setup_and_teardown
    response = client.get(f"/maintainance_status/{estado.ID}", headers=headers)
    assert response.status_code == 200
    logger.info(f"Test detalle_estado_existente ejecutado correctamente para ID={estado.ID}.")

def test_detalle_estado_no_existente():
    response = client.get("/maintainance_status/99999", headers=headers)
    assert response.status_code in (404, 500)
    logger.warning(
        f"Test detalle_estado_no_existente ejecutado: status={response.status_code}, body={response.text}"
    )

def test_listar_estados_error_interno(monkeypatch):
    """
    Prueba para cubrir el error interno al listar estados de mantenimiento.
    """
    def fake_read_all(model):
        raise Exception("Simulated error")
    monkeypatch.setattr(controller, "read_all", fake_read_all)
    response = client.get("/maintainance_status/", headers=headers)
    assert response.status_code == 500
    assert "Simulated error" in response.json()["detail"]
    logger.error("Test listar_estados_error_interno ejecutado correctamente.")

def test_detalle_estado_error_interno(monkeypatch):
    """
    Prueba para cubrir el error interno al consultar el detalle de un estado de mantenimiento.
    """
    def fake_get_by_id(model, id):
        raise Exception("Simulated error")
    monkeypatch.setattr(controller, "get_by_id", fake_get_by_id)
    response = client.get("/maintainance_status/9999", headers=headers)
    assert response.status_code == 500
    assert "Simulated error" in response.json()["detail"]
    logger.error("Test detalle_estado_error_interno ejecutado correctamente.")