import pytest
from fastapi.testclient import TestClient
from backend.app.api.routes.stops_cud_service import app as stops_router
from backend.app.logic.universal_controller_postgres import UniversalController
from backend.app.models.stops import Stop
from backend.app.core.conf import headers
from fastapi import FastAPI

app_for_test = FastAPI()
app_for_test.include_router(stops_router)
client = TestClient(app_for_test)
controller = UniversalController()

@pytest.fixture(autouse=True)
def setup_and_teardown():
    controller.clear_tables()
    yield
    controller.clear_tables()

def test_crear_parada():
    response = client.post("/stops/create", data={
        "id": 1,
        "nombre": "Parada 1",
        "ubicacion": "Ubicación 1"
    }, headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Parada creada exitosamente."

def test_actualizar_parada():
    controller.add(Stop(id=1, nombre="Parada 1", ubicacion="Ubicación 1"))
    response = client.post("/stops/update", data={
        "id": 1,
        "nombre": "Parada Actualizada",
        "ubicacion": "Ubicación Actualizada"
    }, headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Parada actualizada exitosamente."

def test_eliminar_parada():
    controller.add(Stop(id=1, nombre="Parada 1", ubicacion="Ubicación 1"))
    response = client.post("/stops/delete", data={"id": 1}, headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Parada eliminada exitosamente."