import pytest
from fastapi.testclient import TestClient
from backend.app.api.routes.maintainance_status_cud_service import app
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

def test_crear_estado():
    response = client.post("/maintainance_state/create", data={
        "id": 1,
        "tipoestado": "Activo"
    }, headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Estado de mantenimiento creado exitosamente."

def test_actualizar_estado():
    controller.add(MaintainanceState(id=1, tipoestado="Activo"))
    response = client.post("/maintainance_state/update", data={
        "id": 1,
        "tipoestado": "En espera"
    }, headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Estado de mantenimiento actualizado exitosamente."

def test_eliminar_estado():
    controller.add(MaintainanceState(id=1, tipoestado="Activo"))
    response = client.post("/maintainance_state/delete", data={"id": 1}, headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Estado de mantenimiento eliminado exitosamente."