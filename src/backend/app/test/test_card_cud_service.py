import pytest
from fastapi.testclient import TestClient
from src.backend.app.api.routes.card_cud_service import app  # Usamos 'src' para la importación
from src.backend.app.logic.universal_controller_sql import UniversalController
from src.backend.app.models.card import CardCreate, CardOut
from fastapi import HTTPException
from fastapi import FastAPI
app = FastAPI()
# Mock de la clase UniversalController
class MockUniversalController:
    def __init__(self):
        # Datos simulados de tarjetas
        self.cards = {
            1: CardOut(id=1, tipo="tipo_1", balance=100),
            2: CardOut(id=2, tipo="tipo_2", balance=200)
        }

    def add(self, card: CardCreate) -> CardOut:
        """Simula la creación de una tarjeta."""
        new_card = CardOut(id=card.id, tipo=card.tipo, balance=card.balance)
        self.cards[card.id] = new_card
        return new_card

    def get_by_id(self, model, id_: int) -> CardOut:
        """Simula la obtención de una tarjeta por ID."""
        return self.cards.get(id_)

    def update(self, card: CardCreate) -> CardOut:
        """Simula la actualización de una tarjeta."""
        if card.id in self.cards:
            updated_card = CardOut(id=card.id, tipo=card.tipo, balance=card.balance)
            self.cards[card.id] = updated_card
            return updated_card
        raise HTTPException(status_code=404, detail="Card not found")

    def delete(self, card: CardOut):
        """Simula la eliminación de una tarjeta."""
        if card.id in self.cards:
            del self.cards[card.id]
        else:
            raise HTTPException(status_code=404, detail="Card not found")


# Reemplazamos el controlador real por el mock
app.dependency_overrides[UniversalController] = MockUniversalController

# Inicializamos el cliente de pruebas de FastAPI
client = TestClient(app)

@pytest.fixture
def mock_controller():
    """Fixture para el mock del controlador"""
    return MockUniversalController()

def test_create_card(mock_controller):
    # Probamos la creación de una tarjeta
    response = client.post("/card/create", data={"id": 3, "tipo": "tipo_3"})
    assert response.status_code == 200
    assert response.json()["operation"] == "create"
    assert response.json()["success"] is True
    assert response.json()["data"]["id"] == 3

def test_update_card_existing(mock_controller):
    # Probamos la actualización de una tarjeta existente
    response = client.post("/card/update", data={"id": 1, "tipo": "tipo_1_updated"})
    assert response.status_code == 200
    assert response.json()["operation"] == "update"
    assert response.json()["success"] is True
    assert response.json()["data"]["tipo"] == "tipo_1_updated"

def test_update_card_not_found(mock_controller):
    # Probamos la actualización de una tarjeta que no existe
    response = client.post("/card/update", data={"id": 999, "tipo": "tipo_nonexistent"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Card not found"

def test_delete_card_existing(mock_controller):
    # Probamos la eliminación de una tarjeta existente
    response = client.post("/card/delete", data={"id": 2})
    assert response.status_code == 200
    assert response.json()["operation"] == "delete"
    assert response.json()["success"] is True
    assert response.json()["message"] == "Card 2 deleted successfully"

def test_delete_card_not_found(mock_controller):
    # Probamos la eliminación de una tarjeta que no existe
    response = client.post("/card/delete", data={"id": 999})
    assert response.status_code == 404
    assert response.json()["detail"] == "Card not found"

def test_index_create_form(mock_controller):
    # Probamos que la ruta de la plantilla "CrearTarjeta.html" se muestra correctamente
    response = client.get("/card/crear")
    assert response.status_code == 200
    assert "CrearTarjeta.html" in response.text

def test_index_update_form(mock_controller):
    # Probamos que la ruta de la plantilla "ActualizarTarjeta.html" se muestra correctamente
    response = client.get("/card/actualizar")
    assert response.status_code == 200
    assert "ActualizarTarjeta.html" in response.text

def test_index_delete_form(mock_controller):
    # Probamos que la ruta de la plantilla "EliminarTarjeta.html" se muestra correctamente
    response = client.get("/card/eliminar")
    assert response.status_code == 200
    assert "EliminarTarjeta.html" in response.text
