import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from fastapi.staticfiles import StaticFiles

from backend.app.api.routes.card_service.card_query_service import app as card_router
from backend.app.api.routes.card_service import card_query_service
from backend.app.logic.universal_controller_sql import UniversalController
from backend.app.core.conf import headers

from backend.app.models.card import CardCreate
from backend.app.models.user import UserCreate
from backend.app.models.shift import Shift
from backend.app.models.type_card import TypeCardCreate

# Inicializa el controlador real y lo inyecta en el módulo del router
controller = UniversalController()
card_query_service.controller = controller  # Inyección de dependencia

# Setup y Teardown de pruebas
def setup_function():
    controller.clear_tables()

def teardown_function():
    controller.clear_tables()

# Crear app de prueba e incluir el router
app_for_test = FastAPI()
app_for_test.include_router(card_router)
app_for_test.mount("/static", StaticFiles(directory="src/frontend/static"), name="static")
client = TestClient(app_for_test)

# Test GET /card/consultar
def test_consultar_page():
    response = client.get("/card/consultar", headers=headers)
    assert response.status_code == 200
    assert "Consultar Saldo" in response.text

# Test GET /card/tarjetas
def test_get_tarjetas():
    # Carga previa necesaria
    controller.add(TypeCardCreate(ID=1, type="tipo_1"))
    controller.add(TypeCardCreate(ID=2, type="tipo_2"))
    controller.add(TypeCardCreate(ID=3, type="tipo_3"))
    controller.add(TypeCardCreate(ID=4, type="tipo_4"))
    controller.add(Shift(ID=1, TipoTurno="No Aplica"))
    controller.add(UserCreate(
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

    controller.add(CardCreate(ID=3, IDUsuario=1, IDTipoTarjeta=3, Saldo=0.0))
    controller.add(CardCreate(ID=4, IDUsuario=1, IDTipoTarjeta=4, Saldo=10.0))
    controller.add(CardCreate(ID=2, IDUsuario=1, IDTipoTarjeta=2, Saldo=5.0))
    controller.add(CardCreate(ID=1, IDUsuario=1, IDTipoTarjeta=1, Saldo=0.0))
    
    response = client.get("/card/tarjetas", headers=headers)
    data = response.json()

    assert response.status_code == 200
    assert len(data) == 4
    assert data[0]["ID"] == 1
    assert data[1]["IDTipoTarjeta"] == 2

# Test GET /card/tarjeta?ID=... para tarjeta existente
def test_get_tarjeta_existing():
    # Cargar datos necesarios
    controller.add(TypeCardCreate(ID=3, type="tipo_3"))
    controller.add(Shift(ID=1, TipoTurno="No Aplica"))
    controller.add(UserCreate(
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
    controller.add(CardCreate(ID=3, IDUsuario=1, IDTipoTarjeta=3, Saldo=0.0))

    response = client.get("/card/tarjeta?ID=3", headers=headers)

    assert response.status_code == 200
    assert "Detalles de la Tarjeta" in response.text
    assert "3" in response.text
    assert "0" in response.text

# Test GET /card/tarjeta?ID=... para tarjeta no encontrada
def test_get_tarjeta_not_found():
    response = client.get("/card/tarjeta?ID=9999", headers=headers)
    assert response.status_code == 200
