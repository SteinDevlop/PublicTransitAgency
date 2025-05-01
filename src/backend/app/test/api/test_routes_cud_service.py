"""from fastapi import FastAPI
from fastapi.testclient import TestClient
from backend.app.logic.universal_controller_sql import UniversalController
from backend.app.api.routes.routes_cud_service import app as routes_router

def setup_function():
    UniversalController().clear_tables()

def teardown_function():
    UniversalController().clear_tables()

app_for_test = FastAPI()
app_for_test.include_router(routes_router)
client = TestClient(app_for_test)

def test_create_route():
    response = client.post(
        "/routes/create",
        data={
            "route_id": "RUT001",
            "name": "Ruta Principal",
            "origin": "Estación A",
            "destination": "Estación B"
        }
    )
    assert response.status_code == 200
    assert response.json()["success"] is True
    assert response.json()["data"]["route_id"] == "RUT001"
    assert response.json()["data"]["name"] == "Ruta Principal"

def test_update_route_existing():
    # Crear una ruta primero
    client.post(
        "/routes/create",
        data={
            "route_id": "RUT002",
            "name": "Ruta Vieja",
            "origin": "Punto X",
            "destination": "Punto Y"
        }
    )
    # Luego actualizarla
    response = client.post(
        "/routes/update/RUT002",
        data={
            "name": "Ruta Nueva",
            "destination": "Punto Z"
        }
    )
    assert response.status_code == 200
    assert response.json()["success"] is True
    assert response.json()["data"]["name"] == "Ruta Nueva"
    assert response.json()["data"]["destination"] == "Punto Z"

def test_update_route_not_found():
    response = client.post(
        "/routes/update/RUT999",
        data={
            "name": "Ruta Fantasma",
            "origin": "Inicio Inexistente"
        }
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Route not found"

def test_delete_route_existing():
    # Crear una ruta primero
    client.post(
        "/routes/create",
        data={
            "route_id": "RUT003",
            "name": "Ruta Temporal",
            "origin": "Salida 1",
            "destination": "Llegada 1"
        }
    )
    # Luego eliminarla
    response = client.post("/routes/delete/RUT003")
    assert response.status_code == 200
    assert response.json()["success"] is True

def test_delete_route_not_found():
    response = client.post("/routes/delete/RUT999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Route not found"

def test_index_create_form():
    response = client.get("/routes/crear")
    assert response.status_code == 200

def test_index_update_form():
    response = client.get("/routes/actualizar")
    assert response.status_code == 200

def test_index_delete_form():
    response = client.get("/routes/eliminar")
    assert response.status_code == 200"""