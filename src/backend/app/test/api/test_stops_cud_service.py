import pytest
from fastapi.testclient import TestClient
from backend.app.api.routes.stops_cud_service import app as paradas_router
from backend.app.logic.universal_controller_postgres import UniversalController
from backend.app.models.stops import Parada
from backend.app.core.conf import headers
from fastapi import FastAPI

app_for_test = FastAPI()
app_for_test.include_router(paradas_router)
client = TestClient(app_for_test)
controller = UniversalController()

@pytest.fixture(autouse=True)
def setup_and_teardown():
    controller.clear_tables()
    yield
    controller.clear_tables()

def test_crear_parada():
    response = client.post("/paradas/create", data={
        "id": 1,
        "name": "Parada 1",
        "ubication": "Ubicación 1"
    }, headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Parada creada exitosamente."

def test_actualizar_parada_no_existente():
    response = client.post("/paradas/update", data={
        "id": 999,
        "name": "Parada No Existente",
        "ubication": "Sin Ubicación"
    }, headers=headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "Parada no encontrada"

def test_eliminar_parada_no_existente():
    response = client.post("/paradas/delete", data={"id": 999}, headers=headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "Parada no encontrada"