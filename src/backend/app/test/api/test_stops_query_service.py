import pytest
from fastapi.testclient import TestClient
from backend.app.api.routes.stops_query_service import app as stops_router
from backend.app.logic.universal_controller_sql import UniversalController
from backend.app.models.stops import StopCreate

client = TestClient(stops_router)

def setup_function():
    UniversalController().clear_tables()

def test_listar_paradas():
    response = client.get("/stops/")
    assert response.status_code == 200

def test_detalle_parada_existente():
    controller = UniversalController()
    controller.add(StopCreate(stop_id=1, stop_data={"name": "Parada 1", "location": "Ubicación 1"}))
    response = client.get("/stops/1")
    assert response.status_code == 200

def test_detalle_parada_no_existente():
    response = client.get("/stops/999")
    assert response.status_code == 404