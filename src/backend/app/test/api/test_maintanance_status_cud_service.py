import pytest
from fastapi.testclient import TestClient
from backend.app.api.routes.maintainance_status_cud_service import app
from backend.app.models.maintainance_status import MaintainanceStatus
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
    response = client.post("/maintainance_status/create", data={
        "id": 1,
        "type": "Preventivo",  # Campo añadido
        "status": "Activo"     # Campo añadido
    }, headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Estado de mantenimiento creado exitosamente."

def test_actualizar_estado():
    controller.add(MaintainanceStatus(id=1, type="Preventivo", status="Activo"))
    response = client.post("/maintainance_status/update", data={
        "id": 1,
        "type": "Correctivo",  # Valor actualizado
        "status": "Inactivo"  # Valor actualizado
    }, headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Estado de mantenimiento actualizado exitosamente."

def test_eliminar_estado():
    controller.add(MaintainanceStatus(id=1, type="Preventivo", status="Activo"))
    response = client.post("/maintainance_status/delete", data={"id": 1}, headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Estado de mantenimiento eliminado exitosamente."