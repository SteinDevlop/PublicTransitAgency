import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI
from backend.app.api.routes.transport_unit_CUD_service import app as transport_router
from backend.app.logic.universal_controller_sql import UniversalController
from backend.app.models.transport import Transport
app_for_test = FastAPI()
app_for_test.include_router(transport_router)
client = TestClient(app_for_test)

def setup_function():
    UniversalController().clear_tables()

def teardown_function():
    UniversalController().clear_tables()

controller = UniversalController()

def test_crear_unidad():
    response = client.post("/transports/create", data={"id": "1", "type": "Bus", "status": "bien", "ubication": "Garage", "capacity": 50})
    assert response.status_code == 200

def test_actualizar_unidad():
    controller.add(Transport(id="1", type="Bus", status="bien", ubication="Garage", capacity=50))
    response = client.post("/transports/update", data={"id": "1", "type": "Bus", "status": "mantenimiento", "ubication": "Garage", "capacity": 50})
    assert response.status_code == 200

def test_eliminar_unidad():
    controller.add(Transport(id="1", type="Bus", status="bien", ubication="Garage", capacity=50))
    response = client.post("/transports/delete", data={"id": "1"})
    assert response.status_code == 200