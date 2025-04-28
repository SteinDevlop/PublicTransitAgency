import pytest
from fastapi.testclient import TestClient
from src.backend.app.logic.universal_controller_sql import UniversalController
from src.backend.app.models.type_card import TypeCardOut, TypeCardCreate
from fastapi import HTTPException
from fastapi import FastAPI
from src.backend.app.api.routes.type_card_query_service import app as typecard_router

app_for_test = FastAPI()
app_for_test.include_router(typecard_router)

client = TestClient(app_for_test)

# Mock de la clase UniversalController
class MockUniversalController:
    def __init__(self):
        # Datos simulados de tipos de tarjeta
        self.typecards = {
            1: TypeCardOut(id=3, type="lolu"),  # Agregar el tipo de tarjeta esperado con id=3
        }

    def read_all(self, model):
        """Simula obtener todos los tipos de tarjeta"""
        return list(self.typecards.values())

    def get_by_id(self, model, id_: int):
        """Simula obtener un tipo de tarjeta por ID"""
        return self.typecards.get(id_)


@pytest.fixture
def mock_controller():
    """Fixture para el mock del controlador"""
    return MockUniversalController()

def test_read_all(mock_controller):
    """Prueba que la ruta '/typecards/' devuelve todos los tipos de tarjeta."""
    response = client.get("/typecard/typecards/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == 3
    assert data[0]["type"] == "lolu"

def test_get_by_id(mock_controller):
    """Prueba que la ruta '/typecard/{id}' devuelve el tipo de tarjeta correcto."""
    response = client.get("/typecard/3")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 3
    assert data["type"] == "lolu"

def test_get_by_id_not_found(mock_controller):
    """Prueba que la ruta '/typecard/{id}' devuelve un error 404 si no se encuentra el tipo de tarjeta."""
    response = client.get("/typecard/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Not found"}
