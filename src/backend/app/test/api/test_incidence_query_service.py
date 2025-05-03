from fastapi.testclient import TestClient
from backend.app.api.routes.incidence_query_service import app as incidence_router
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

def test_listar_incidencias():
    controller.add(Incidence(ID=1, IDTicket=101, Descripcion="Falla técnica", Tipo="Técnica", IDUnidad=10))
    response = client.get("/incidence/")
    assert response.status_code == 200
    assert "Falla técnica" in response.text

def test_detalle_incidencia_existente():
    controller.add(Incidence(ID=1, IDTicket=101, Descripcion="Falla técnica", Tipo="Técnica", IDUnidad=10))
    response = client.get("/incidence/1")
    assert response.status_code == 200
    assert "Falla técnica" in response.text

def test_detalle_incidencia_no_existente():
    response = client.get("/incidence/999")
    assert response.status_code == 404