import pytest
from fastapi.testclient import TestClient
from backend.app.api.routes.transport_unit_cud_service import app as transports_router
from backend.app.models.transport import TransportUnitCreate
from backend.app.logic.universal_controller_sql import UniversalController

client = TestClient(transports_router)

def setup_function():
    UniversalController().clear_tables()

def test_crear_unidad():
    response = client.post("/transports/create", data={"id": "1", "type": "Bus", "status": "bien", "ubication": "Garage", "capacity": 50})
    assert response.status_code == 303

def test_actualizar_unidad():
    controller = UniversalController()
    controller.add(TransportUnitCreate(id="1", type="Bus", status="bien", ubication="Garage", capacity=50))
    response = client.post("/transports/update", data={"id": "1", "type": "Bus", "status": "mantenimiento", "ubication": "Garage", "capacity": 50})
    assert response.status_code == 303

def test_eliminar_unidad():
    controller = UniversalController()
    controller.add(TransportUnitCreate(id="1", type="Bus", status="bien", ubication="Garage", capacity=50))
    response = client.post("/transports/delete", data={"id": "1"})
    assert response.status_code == 303