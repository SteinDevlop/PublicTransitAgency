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

def test_listar_incidencias():
    controller.add(Incidence(ID=1, IDTicket=101, Descripcion="Falla técnica", Tipo="Técnica", IDUnidad=10))
    response = client.get("/incidence/")
    assert response.status_code == 200
    assert "Falla técnica" in response.text

def test_eliminar_incidencia():
    controller.add(Incidence(id=1, description="Falla técnica", type="Técnica", status="Pendiente", ticket_id=101))
    response = client.post("/incidence/delete", data={"id": 1})
    assert response.status_code == 200