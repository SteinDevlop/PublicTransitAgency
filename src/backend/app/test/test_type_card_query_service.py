import pytest
from fastapi.testclient import TestClient
from src.backend.app.api.routes.type_card_query_service import app  # Usamos 'src' para la importación
from src.backend.app.logic.universal_controller_sql import UniversalController
from src.backend.app.models.type_card import TypeCardOut, TypeCardCreate
from fastapi import HTTPException

# Mock de la clase UniversalController
class MockUniversalController:
    def __init__(self):
        # Datos simulados de tipos de tarjeta
        self.typecards = {
            1: TypeCardOut(id=1, type="type_1"),
            2: TypeCardOut(id=2, type="type_2")
        }

    def read_all(self, model):
        """Simula obtener todos los tipos de tarjeta"""
        return list(self.typecards.values())

    def get_by_id(self, model, id_: int):
        """Simula obtener un tipo de tarjeta por ID"""
        return self.typecards.get(id_)

# Reemplazamos el controlador real por el mock
app.dependency_overrides[UniversalController] = MockUniversalController

# Inicializamos el cliente de pruebas de FastAPI
client = TestClient(app)

@pytest.fixture
def mock_controller():
    """Fixture para el mock del controlador"""
    return MockUniversalController()

def test_read_all(mock_controller):
    """Prueba que la ruta '/typecards/' devuelve todos los tipos de tarjeta."""
    response = client.get("/typecard/typecards/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2  # Tenemos 2 tipos de tarjeta en el mock
    assert data[0]["id"] == 1
    assert data[1]["type"] == "type_2"

def test_get_by_id(mock_controller):
    """Prueba que la ruta '/typecard/{id}' devuelve el tipo de tarjeta correcto."""
    response = client.get("/typecard/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["type"] == "type_1"

def test_get_by_id_not_found(mock_controller):
    """Prueba que la ruta '/typecard/{id}' devuelve un error 404 si no se encuentra el tipo de tarjeta."""
    response = client.get("/typecard/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Not found"}

