import pytest
from fastapi.testclient import TestClient
from backend.app.api.routes.stops_query_service import app as stops_router
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

def test_listar_paradas():
    controller.add(Stop(id=999, nombre="Parada 999", ubicacion="Ubicación 999"))
    response = client.get("/stops/", headers=headers)
    assert response.status_code == 200
    assert "Parada 999" in response.text

def test_detalle_parada_existente():
    controller.add(Stop(id=999, nombre="Parada 999", ubicacion="Ubicación 999"))
    response = client.get("/stops/999", headers=headers)
    assert response.status_code == 200
    assert "Parada 999" in response.text

def test_detalle_parada_no_existente():
    response = client.get("/stops/998", headers=headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "Parada no encontrada"