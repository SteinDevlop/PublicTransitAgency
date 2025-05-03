from fastapi.testclient import TestClient
from backend.app.api.routes.maintainance_status_CUD_service import app as status_router
from backend.app.logic.universal_controller_sql import UniversalController
from backend.app.models.maintainance_status import MaintainanceStatus
from fastapi import FastAPI

app_for_test = FastAPI()
app_for_test.include_router(status_router)
client = TestClient(app_for_test)
controller = UniversalController()

def setup_function():
    controller.clear_tables()

def teardown_function():
    controller.clear_tables()

def test_crear_estado():
    response = client.post("/maintainance_status/create", data={
        "id": 1,
        "unit": "Unidad 1",
        "type": "Preventivo",
        "status": "Pendiente"
    })
    assert response.status_code == 200

def test_actualizar_estado():
    controller.add(MaintainanceStatus(id=1, unit="Unidad 1", type="Preventivo", status="Pendiente"))
    response = client.post("/maintainance_status/update", data={
        "id": 1,
        "unit": "Unidad 1",
        "type": "Correctivo",
        "status": "En Proceso"
    })
    assert response.status_code == 200

def test_eliminar_estado():
    controller.add(MaintainanceStatus(id=1, unit="Unidad 1", type="Preventivo", status="Pendiente"))
    response = client.post("/maintainance_status/delete", data={"id": 1})
    assert response.status_code == 200