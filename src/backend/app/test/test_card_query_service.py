import pytest
from fastapi.testclient import TestClient
from src.backend.app.api.routes.card_query_service import app  # Usamos 'src' para la importación
from src.backend.app.logic.universal_controller_sql import UniversalController
from src.backend.app.models.card import CardOut
from fastapi import HTTPException

# Mock de la clase UniversalController
class MockUniversalController:
    def __init__(self):
        # Datos simulados de tarjetas
        self.cards = {
            1: CardOut(id=1, tipo="tipo_1", balance=100),
            2: CardOut(id=2, tipo="tipo_2", balance=200)
        }

    def read_all(self, model):
        """Simula la lectura de todas las tarjetas."""
        return [card.dict() for card in self.cards.values()]

    def get_by_id(self, model, id_: int) -> CardOut:
        """Simula la obtención de una tarjeta por ID."""
        return self.cards.get(id_)

# Reemplazamos el controlador real por el mock
app.dependency_overrides[UniversalController] = MockUniversalController

# Inicializamos el cliente de pruebas de FastAPI
client = TestClient(app)

@pytest.fixture
def mock_controller():
    """Fixture para el mock del controlador"""
    return MockUniversalController()

def test_consultar_page(mock_controller):
    """Prueba que la ruta '/consultar' devuelve la plantilla 'ConsultarTarjeta.html' correctamente."""
    response = client.get("/card/consultar")
    assert response.status_code == 200
    assert "ConsultarTarjeta.html" in response.text

def test_get_tarjetas(mock_controller):
    """Prueba que la ruta '/tarjetas' devuelve correctamente todas las tarjetas."""
    response = client.get("/card/tarjetas")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2  # Esperamos que haya 2 tarjetas en el mock
    assert data[0]["id"] == 1
    assert data[1]["id"] == 2

def test_get_tarjeta_existing(mock_controller):
    """Prueba que la ruta '/tarjeta' devuelve la tarjeta correctamente cuando existe."""
    response = client.get("/card/tarjeta?id=1")
    assert response.status_code == 200
    assert "tipo_1" in response.text  # Verificamos que el tipo de tarjeta 'tipo_1' está en la respuesta
    assert "100" in response.text  # Verificamos que el saldo '100' está en la respuesta

def test_get_tarjeta_not_found(mock_controller):
    """Prueba que la ruta '/tarjeta' devuelve un valor 'None' cuando no encuentra la tarjeta."""
    response = client.get("/card/tarjeta?id=999")  # ID que no existe
    assert response.status_code == 200
    assert "None" in response.text  # Verificamos que 'None' es mostrado para el id, tipo y saldo
    assert "None" in response.text
