from fastapi.testclient import TestClient
from backend.app.api.routes.routes_query_service import app as routes_router
from backend.app.logic.universal_controller_sql import UniversalController
from backend.app.models.routes import Route
from fastapi import FastAPI

app_for_test = FastAPI()
app_for_test.include_router(routes_router)
client = TestClient(app_for_test)
controller = UniversalController()

def setup_function():
    controller.clear_tables()

def teardown_function():
    controller.clear_tables()

def test_listar_rutas():
    controller.add(Route(ID=1, IDHorario=10, Nombre="Ruta 1"))
    response = client.get("/routes/")
    assert response.status_code == 200
    assert "Ruta 1" in response.text

def test_detalle_ruta_existente():
    controller.add(Route(ID=1, IDHorario=10, Nombre="Ruta 1"))
    response = client.get("/routes/1")
    assert response.status_code == 200
    assert "Ruta 1" in response.text

def test_detalle_ruta_no_existente():
    response = client.get("/routes/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Ruta no encontrada"