import pytest
from fastapi.testclient import TestClient
from backend.app.api.routes.transport_unit_query_service import app as transports_router
from backend.app.logic.universal_controller_sql import UniversalController
from backend.app.models.transport import Transport
from fastapi import FastAPI

app_for_test = FastAPI()
app_for_test.include_router(transports_router)
client = TestClient(app_for_test)
controller = UniversalController()
def setup_function():
    UniversalController().clear_tables()

def teardown_function():
    UniversalController().clear_tables()
def test_listar_unidades():
    response = client.get("/transports/")
    assert response.status_code == 200

def test_detalle_unidad_existente():
    controller.add(Transport(id="1", type="Bus", status="bien", ubication="Garage", capacity=50))
    response = client.get("/transports/1")
    assert response.status_code == 200

def test_detalle_unidad_no_existente():
    response = client.get("/transports/999")
    assert response.status_code == 404