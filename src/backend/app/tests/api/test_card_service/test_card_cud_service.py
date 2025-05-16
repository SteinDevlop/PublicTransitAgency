from fastapi import FastAPI 
from fastapi.staticfiles import StaticFiles
from fastapi.testclient import TestClient
from backend.app.logic.universal_controller_sql import UniversalController
from backend.app.api.routes.card_service import card_cud_service  # Importamos el módulo, no solo el `app`
from backend.app.core.conf import headers
from backend.app.models.user import UserCreate
from backend.app.models.shift import Shift
from backend.app.models.type_card import TypeCardCreate
from backend.app.models.card import CardCreate

# Crear instancia del controlador que se usará en pruebas
test_controller = UniversalController()

# Sobrescribir el controlador usado en el módulo de rutas
card_cud_service.controller = test_controller

# Limpiar base de datos
def setup_function():
    test_controller.clear_tables()

def teardown_function():
    test_controller.clear_tables()

# App de prueba
app_for_test = FastAPI()
app_for_test.include_router(card_cud_service.app)
app_for_test.mount("/static", StaticFiles(directory="src/frontend/static"), name="static")

client = TestClient(app_for_test)

def test_create_card():
    test_controller.add(TypeCardCreate(ID=1, type="Estandar"))
    test_controller.add(Shift(ID=1, TipoTurno="No Aplica"))
    test_controller.add(UserCreate(
        ID=1,
        Identificacion=11022311,
        Nombre="Kenan",
        Apellido="Jarrus",
        Correo="msjedi@yoda.com",
        Contrasena="hera",
        IDRolUsuario=1,
        IDTurno=1,
        IDTarjeta=1
    ))
    response = client.post("/card/create", data={"ID": 15, "IDUsuario": 1, "IDTipoTarjeta": 1}, headers=headers)
    assert response.status_code == 200
    assert response.json()["data"]["ID"] == 15
    assert response.json()["data"]["Saldo"] == 0

def test_update_card_existing():
    test_controller.add(TypeCardCreate(ID=1, type="Estandar"))
    test_controller.add(Shift(ID=1, TipoTurno="No Aplica"))
    test_controller.add(UserCreate(
        ID=1,
        Identificacion=11022311,
        Nombre="Kenan",
        Apellido="Jarrus",
        Correo="msjedi@yoda.com",
        Contrasena="hera",
        IDRolUsuario=1,
        IDTurno=1,
        IDTarjeta=1
    ))
    test_controller.add(CardCreate(ID=20, IDUsuario=1, IDTipoTarjeta=1, Saldo=10))

    response = client.post("/card/update", data={"ID": 20, "IDUsuario": 1, "IDTipoTarjeta": 2}, headers=headers)
    assert response.status_code == 200
    assert response.json()["data"]["IDTipoTarjeta"] == 2

def test_update_card_not_found():
    response = client.post("/card/update", data={"ID": 999, "IDUsuario": 1, "IDTipoTarjeta": 1}, headers=headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "Card not found"

def test_delete_card_existing():
    test_controller.add(TypeCardCreate(ID=1, type="Estandar"))
    test_controller.add(Shift(ID=1, TipoTurno="No Aplica"))
    test_controller.add(UserCreate(
        ID=1,
        Identificacion=11022311,
        Nombre="Kenan",
        Apellido="Jarrus",
        Correo="msjedi@yoda.com",
        Contrasena="hera",
        IDRolUsuario=1,
        IDTurno=1,
        IDTarjeta=1
    ))
    test_controller.add(CardCreate(ID=30, IDUsuario=1, IDTipoTarjeta=1, Saldo=0))

    response = client.post("/card/delete", data={"ID": 30}, headers=headers)
    assert response.status_code == 200
    assert "deleted" in response.json()["message"]

def test_delete_card_not_found():
    response = client.post("/card/delete", data={"ID": 999}, headers=headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "Card not found"

