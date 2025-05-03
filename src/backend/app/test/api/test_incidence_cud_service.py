from fastapi.testclient import TestClient
from backend.app.api.routes.incidence_CUD_service import app as incidence_router
from backend.app.logic.universal_controller_sql import UniversalController
from backend.app.models.incidence import Incidence
from fastapi import FastAPI

app_for_test = FastAPI()
app_for_test.include_router(incidence_router)
client = TestClient(app_for_test)
controller = UniversalController()

def setup_function():
    controller.clear_tables()

def teardown_function():
    controller.clear_tables()

def test_crear_incidencia():
    response = client.post("/incidence/create", data={
        "ID": 1,
        "IDTicket": 101,
        "Descripcion": "Falla técnica",
        "Tipo": "Técnica",
        "IDUnidad": 10
    })
    assert response.status_code == 200

def test_actualizar_incidencia():
    controller.add(Incidence(ID=1, IDTicket=101, Descripcion="Falla técnica", Tipo="Técnica", IDUnidad=10))
    response = client.post("/incidence/update", data={
        "ID": 1,
        "IDTicket": 102,
        "Descripcion": "Falla corregida",
        "Tipo": "Operativa",
        "IDUnidad": 20
    })
    assert response.status_code == 200

def test_eliminar_incidencia():
    controller.add(Incidence(ID=1, IDTicket=101, Descripcion="Falla técnica", Tipo="Técnica", IDUnidad=10))
    response = client.post("/incidence/delete", data={"ID": 1})
    assert response.status_code == 200