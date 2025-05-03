from fastapi.testclient import TestClient
from backend.app.api.routes.stops_query_service import app as stops_router
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

def test_listar_paradas():
    controller.add(Stop(ID=1, Nombre="Parada 1", Ubicacion="Ubicación 1"))
    response = client.get("/stops/")
    assert response.status_code == 200
    assert "Parada 1" in response.text

def test_detalle_parada_existente():
    controller.add(Stop(ID=1, Nombre="Parada 1", Ubicacion="Ubicación 1"))
    response = client.get("/stops/1")
    assert response.status_code == 200
    assert "Parada 1" in response.text

def test_detalle_parada_no_existente():
    response = client.get("/stops/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Parada no encontrada"