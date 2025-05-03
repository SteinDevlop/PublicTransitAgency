from fastapi.testclient import TestClient
from backend.app.api.routes.incidence_CUD_service import app as incidences_router
from backend.app.logic.universal_controller_sql import UniversalController
from backend.app.models.incidence import Incidence
from fastapi import FastAPI

app_for_test = FastAPI()
app_for_test.include_router(incidences_router)
client = TestClient(app_for_test)
controller = UniversalController()

def setup_function():
    controller.clear_tables()

def teardown_function():
    controller.clear_tables()

def test_crear_incidencia():
    response = client.post("/incidences/create", data={"ID": 1, "IDTicket": 1, "Descripcion": "Test", "Tipo": "Tipo1", "IDUnidad": 1})
    assert response.status_code == 200

def test_actualizar_incidencia():
    controller.add(Incidence(ID=1, IDTicket=1, Descripcion="Test", Tipo="Tipo1", IDUnidad=1))
    response = client.post("/incidences/update", data={"ID": 1, "IDTicket": 1, "Descripcion": "Updated", "Tipo": "Tipo2", "IDUnidad": 2})
    assert response.status_code == 200

def test_eliminar_incidencia():
    controller.add(Incidence(ID=1, IDTicket=1, Descripcion="Test", Tipo="Tipo1", IDUnidad=1))
    response = client.post("/incidences/delete", data={"ID": 1})
    assert response.status_code == 200