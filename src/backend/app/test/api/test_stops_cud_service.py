from fastapi.testclient import TestClient
from backend.app.api.routes.stops_CUD_service import app as stops_router
from backend.app.logic.universal_controller_sql import UniversalController
from backend.app.models.stops import Stop
from fastapi import FastAPI

app_for_test = FastAPI()
app_for_test.include_router(stops_router)
client = TestClient(app_for_test)
controller = UniversalController()

def setup_function():
    controller.clear_tables()

def teardown_function():
    controller.clear_tables()

def test_crear_parada():
    response = client.post("/stops/create", data={"ID": 1, "Nombre": "Parada 1", "Ubicacion": "Ubicación 1"})
    assert response.status_code == 200

def test_actualizar_parada():
    controller.add(Stop(ID=1, Nombre="Parada 1", Ubicacion="Ubicación 1"))
    response = client.post("/stops/update", data={"ID": 1, "Nombre": "Parada Actualizada", "Ubicacion": "Ubicación Actualizada"})
    assert response.status_code == 200

def test_eliminar_parada():
    controller.add(Stop(ID=1, Nombre="Parada 1", Ubicacion="Ubicación 1"))
    response = client.post("/stops/delete", data={"ID": 1})
    assert response.status_code == 200