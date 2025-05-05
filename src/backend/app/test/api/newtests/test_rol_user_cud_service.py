from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.testclient import TestClient
from backend.app.logic.universal_controller_postgres import UniversalController
from backend.app.api.routes.rol_user_cud_service import app as roluser_router  # Importa bien
from backend.app.core.conf import headers
# Limpieza de base de datos antes y después de cada test
def setup_function():
    UniversalController().clear_tables()

def teardown_function():
    UniversalController().clear_tables()
# Creamos la app de prueba
app_for_test = FastAPI()
app_for_test.include_router(roluser_router)
app_for_test.mount("/static", StaticFiles(directory="src/frontend/static"), name="static")

# Cliente de prueba
client = TestClient(app_for_test)

def test_create_roluser():
    response = client.post("/roluser/create", data={"id":1,"type":"pasajero"},headers=headers)
    assert response.status_code == 200

def test_update_roluser_existing():
    # Crear el registro primero
    client.post("/roluser/create", data={"id":2,"type":"operario"},headers=headers)
    
    # Luego actualizarlo
    response = client.post("/roluser/update", data={"id":2,"type":"conductor"},headers=headers)
    assert response.status_code == 200

def test_update_roluser_not_found():
    response = client.post("/roluser/update", data={"id": 99,"type":"administrador"},headers=headers) 
    assert response.status_code == 404
    assert response.json()["detail"] == "RolUser not found"

def test_delete_roluser_existing():
    # Crear el registro primero
    client.post("/roluser/create", data={"id":44,"type":"system"},headers=headers)
    # Luego eliminarlo
    response = client.post("/roluser/delete", data={"id": 44},headers=headers)
    assert response.status_code == 200

def test_delete_roluser_not_found():
    response = client.post("/roluser/delete", data={"id": 999},headers=headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "RolUser not found"

def test_index_create_form():
    response = client.get("/roluser/crear",headers=headers)
    assert response.status_code == 200

def test_index_update_form():
    response = client.get("/roluser/actualizar",headers=headers)
    assert response.status_code == 200

def test_index_delete_form():
    response = client.get("/roluser/eliminar",headers=headers)
    assert response.status_code == 200
