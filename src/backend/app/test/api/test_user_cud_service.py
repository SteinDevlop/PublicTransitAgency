from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.testclient import TestClient
from backend.app.logic.universal_controller_postgres import UniversalController
from backend.app.api.routes.user_cud_service import app as user_router  # Importa bien
from backend.app.core.conf import headers
# Limpieza de base de datos antes y después de cada test
def setup_function():
    UniversalController().clear_tables()

def teardown_function():
    UniversalController().clear_tables()
# Creamos la app de prueba
app_for_test = FastAPI()
app_for_test.include_router(user_router)
app_for_test.mount("/static", StaticFiles(directory="src/frontend/static"), name="static")

# Cliente de prueba
client = TestClient(app_for_test)

def test_create_user():
    response = client.post("/user/create", data={"id":1,"identification":99,"name":"aa","lastname":"bb",
                                                 "email":"prueba12121@gmail.com", "password":"1234@1234Aasss",
                                                    "idtype_user":1,"idturn":1},headers=headers)
    assert response.status_code == 200

def test_update_user_existing():
    # Crear el registro primero
    client.post("/user/create", data={"id":5,"identification":33,"name":"bb","lastname":"cc",
                                                 "email":"prueba@gmail.com", "password":"1234@1234Aasss",
                                                    "idtype_user":2,"idturn":1},headers=headers)
    
    # Luego actualizarlo
    response = client.post("/user/update", data={"id":5,"identification":33,"name":"bb","lastname":"cc",
                                                 "email":"prueba@gmail.com", "password":"1234@1234Aasss",
                                                    "idtype_user":2,"idturn":1},headers=headers)
    assert response.status_code == 200

def test_update_user_not_found():
    response = client.post("/user/update", data={"id": 99, "identification":99,"name":"aa","lastname":"bb",
                                                 "email":"prueba@gmail.com", "password":"1234@1234Aasss",
                                                    "idtype_user":1,"idturn":1},headers=headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"

def test_delete_user_existing():
    # Crear el registro primero
    client.post("/user/create", data={"id":44,"identification":11,"name":"aa","lastname":"bb",
                                                 "email":"prueba@gmail.com", "password":"1234@1234Aasss",
                                                    "idtype_user":1,"idturn":1},headers=headers)
    # Luego eliminarlo
    response = client.post("/user/delete", data={"id": 44},headers=headers)
    assert response.status_code == 200

def test_delete_user_not_found():
    response = client.post("/user/delete", data={"id": 999},headers=headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"

def test_index_create_form():
    response = client.get("/user/crear",headers=headers)
    assert response.status_code == 200

def test_index_update_form():
    response = client.get("/user/actualizar",headers=headers)
    assert response.status_code == 200

def test_index_delete_form():
    response = client.get("/user/eliminar",headers=headers)
    assert response.status_code == 200
