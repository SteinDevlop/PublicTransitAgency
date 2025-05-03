from fastapi.testclient import TestClient
from backend.app.api.routes.routes_CUD_service import app as routes_router
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

def test_crear_ruta():
    response = client.post("/routes/create", data={
        "ID": 1,
        "IDHorario": 10,
        "Nombre": "Ruta 1"
    })
    assert response.status_code == 200

def test_actualizar_ruta():
    controller.add(Route(ID=1, IDHorario=10, Nombre="Ruta 1"))
    response = client.post("/routes/update", data={
        "ID": 1,
        "IDHorario": 20,
        "Nombre": "Ruta Actualizada"
    })
    assert response.status_code == 200

def test_eliminar_ruta():
    controller.add(Route(ID=1, IDHorario=10, Nombre="Ruta 1"))
    response = client.post("/routes/delete", data={"ID": 1})
    assert response.status_code == 200