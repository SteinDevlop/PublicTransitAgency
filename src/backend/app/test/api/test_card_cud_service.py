from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.testclient import TestClient
from backend.app.logic.universal_controller_sql import UniversalController
from backend.app.api.routes.card_cud_service import app as card_router  # Importa bien
from backend.app.core.conf import headers
from backend.app.models.user import UserCreate, UserOut
from backend.app.models.shift import Shift
from backend.app.models.type_card import TypeCardCreate, TypeCardOut
# Limpieza de base de datos antes y después de cada test
controller = UniversalController()
def setup_function():
    controller.clear_tables()

def teardown_function():
    controller.clear_tables()
# Creamos la app de prueba
app_for_test = FastAPI()
app_for_test.include_router(card_router)
app_for_test.mount("/static", StaticFiles(directory="src/frontend/static"), name="static")

# Cliente de prueba
client = TestClient(app_for_test)

def test_create_card():
    controller.add(TypeCardCreate(id=1,tipo="Estandar"))
    controller.add(Shift(ID=1,TipoTurno="No Aplica"))
    controller.add(UserCreate(id= 1,identification= 11022311,name= "Kenan",lastname= "Jarrus",email= "msjedi@yoda.com",password= "hera",idtype_user= 1,idturn= 1))
    
    response = client.post("/card/create", data={"id": 15, "idusuario": 1,"idtipotarjeta": 1,"saldo":0},headers=headers)
    assert response.status_code == 200

def test_update_card_existing():
    # Crear el registro primero
    client.post("/card/create", data={"id": 15, "tipo": "tipo_original"},headers=headers)
    
    # Luego actualizarlo
    response = client.post("/card/update", data={"id": 15, "tipo": "tipo_1_updated"},headers=headers)
    assert response.status_code == 200

def test_update_card_not_found():
    response = client.post("/card/update", data={"id": 999, "tipo": "tipo_nonexistent"},headers=headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "Card not found"

def test_delete_card_existing():
    # Crear el registro primero
    client.post("/card/create", data={"id": 15, "tipo": "tipo_para_borrar"},headers=headers)
    
    # Luego eliminarlo
    response = client.post("/card/delete", data={"id": 15},headers=headers)
    assert response.status_code == 200
def test_delete_card_not_found():
    response = client.post("/card/delete", data={"id": 999},headers=headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "Card not found"

def test_index_create_form():
    response = client.get("/card/crear",headers=headers)
    assert response.status_code == 200

def test_index_update_form():
    response = client.get("/card/actualizar",headers=headers)
    assert response.status_code == 200

def test_index_delete_form():
    response = client.get("/card/eliminar",headers=headers)
    assert response.status_code == 200
