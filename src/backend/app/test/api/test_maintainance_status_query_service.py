from fastapi.testclient import TestClient
from backend.app.api.routes.maintainance_status_query_service import app as status_router
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

def test_listar_estados():
    controller.add(MaintainanceStatus(id=1, unit="Unidad 1", type="Preventivo", status="Pendiente"))
    response = client.get("/maintainance_status/")
    assert response.status_code == 200
    assert "Unidad 1" in response.text

def test_detalle_estado_existente():
    controller.add(MaintainanceStatus(id=1, unit="Unidad 1", type="Preventivo", status="Pendiente"))
    response = client.get("/maintainance_status/1")
    assert response.status_code == 200
    assert "Unidad 1" in response.text

def test_detalle_estado_no_existente():
    response = client.get("/maintainance_status/999")
    assert response.status_code == 404