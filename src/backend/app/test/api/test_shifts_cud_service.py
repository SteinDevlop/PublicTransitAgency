import pytest
from fastapi.testclient import TestClient
from backend.app.api.routes.shifts_cud_service import app as shifts_router
from backend.app.logic.universal_controller_postgres import UniversalController
from backend.app.models.shift import Shift
from backend.app.core.conf import headers
from fastapi import FastAPI

app_for_test = FastAPI()
app_for_test.include_router(shifts_router)
client = TestClient(app_for_test)
controller = UniversalController()

@pytest.fixture(autouse=True)
def setup_and_teardown():
    controller.clear_tables()
    yield
    controller.clear_tables()

def test_crear_turno():
    response = client.post("/shifts/create", data={
        "id": 1,
        "tipoturno": "Diurno"
    }, headers=headers)
    assert response.status_code == 200
    #assert response.json()["message"] == "Turno creado exitosamente."

def test_actualizar_turno():
    controller.add(Shift(id=1, tipoturno="Diurno"))
    response = client.post("/shifts/update", data={
        "id": 1,
        "tipoturno": "Nocturno"
    }, headers=headers)
    assert response.status_code == 200
    #assert response.json()["message"] == "Turno actualizado exitosamente."

def test_eliminar_turno():
    controller.add(Shift(id=1, tipoturno="Diurno"))
    response = client.post("/shifts/delete", data={"id": 1}, headers=headers)
    assert response.status_code == 200
    #assert response.json()["message"] == "Turno eliminado exitosamente."