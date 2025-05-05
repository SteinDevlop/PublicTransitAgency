import pytest
from fastapi.testclient import TestClient
from backend.app.api.routes.maintainance_status_query_service import app
from backend.app.models.maintainance_status import MaintainanceState
from backend.app.logic.universal_controller_postgres import UniversalController
from backend.app.core.conf import headers

client = TestClient(app)
controller = UniversalController()

@pytest.fixture(autouse=True)
def limpiar_bd():
    controller.clear_tables()
    yield
    controller.clear_tables()

def test_listar_estados():
    controller.add(MaintainanceState(id=1, tipoestado="Activo"))
    response = client.get("/maintainance_state/", headers=headers)
    assert response.status_code == 200
    assert "Activo" in response.text

def test_detalle_estado_existente():
    controller.add(MaintainanceState(id=1, tipoestado="Activo"))
    response = client.get("/maintainance_state/1", headers=headers)
    assert response.status_code == 200
    assert "Activo" in response.text

def test_detalle_estado_no_existente():
    response = client.get("/maintainance_state/999", headers=headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "Estado de mantenimiento no encontrado"