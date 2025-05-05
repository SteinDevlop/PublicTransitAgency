import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from fastapi.staticfiles import StaticFiles
from backend.app.api.routes.card_query_service import app as card_router
from backend.app.logic.universal_controller_postgres import UniversalController
from backend.app.core.conf import headers
from backend.app.models.card import CardCreate

# Setup y Teardown de pruebas
def setup_function():
    UniversalController().clear_tables()

def teardown_function():
    UniversalController().clear_tables()

# Crear app de prueba e incluir el router
app_for_test = FastAPI()
app_for_test.include_router(card_router)
app_for_test.mount("/static", StaticFiles(directory="src/frontend/static"), name="static")
client = TestClient(app_for_test)

# Mock del controlador de tarjetas
class MockControllerCard:
    def __init__(self):
        self.cards = []

    def add(self, card):
        self.cards.append(card)

    def read_all(self, *args, **kwargs):
        return sorted([card.__dict__ for card in self.cards], key=lambda c: c["id"])

    def get_by_id(self, card_id, *args, **kwargs):
        for card in self.cards:
            if card.id == card_id:
                class MockCard:
                    def to_dict(inner_self):
                        return card.__dict__
                return MockCard()
        return None

# Patching automático usando fixture
@pytest.fixture(autouse=True)
def override_controller(monkeypatch):
    from backend.app.api.routes import card_query_service
    card_query_service.controller = MockControllerCard()
    global controller
    controller = card_query_service.controller

# Test GET /card/consultar
def test_consultar_page():
    response = client.get("/card/consultar", headers=headers)
    assert response.status_code == 200
    assert "Consultar Saldo" in response.text

# Test GET /card/tarjetas
def test_get_tarjetas():
    controller.add(CardCreate(id=3, tipo="tipo_3", balance=0.0))
    controller.add(CardCreate(id=4, tipo="tipo_4", balance=10.0))
    controller.add(CardCreate(id=2, tipo="tipo_2", balance=5.0))
    controller.add(CardCreate(id=1, tipo="tipo_1", balance=0.0))
    
    response = client.get("/card/tarjetas", headers=headers)
    data = response.json()

    assert response.status_code == 200
    assert len(data) == 4
    assert data[0]["id"] == 1
    assert data[1]["tipo"] == "tipo_2"

# Test GET /card/tarjeta?id=... para tarjeta existente
def test_get_tarjeta_existing():
    controller.add(CardCreate(id=3, tipo="tipo_3", balance=0.0))

    response = client.get("/card/tarjeta?id=3", headers=headers)

    assert response.status_code == 200
    assert "Detalles de la Tarjeta" in response.text
    assert "tipo_3" in response.text
    assert "$0.0" in response.text  # Asegúrate de verificar el balance correctamente en el HTML

# Test GET /card/tarjeta?id=... para tarjeta no encontrada
def test_get_tarjeta_not_found():
    response = client.get("/card/tarjeta?id=9999", headers=headers)
    assert response.status_code == 200
    assert "None" in response.text
