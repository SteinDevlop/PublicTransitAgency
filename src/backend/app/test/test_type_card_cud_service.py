import pytest
from fastapi.testclient import TestClient
from src.backend.app.api.routes.type_card_cud_service import app  # Usamos 'src' para la importación
from src.backend.app.logic.universal_controller_sql import UniversalController
from src.backend.app.models.type_card import TypeCardOut, TypeCardCreate
from fastapi import HTTPException
from fastapi import FastAPI
app = FastAPI()
# Mock de la clase UniversalController
class MockUniversalController:
    def __init__(self):
        # Datos simulados de tipos de tarjeta
        self.typecards = {
            1: TypeCardOut(id=1, type="type_1"),
            2: TypeCardOut(id=2, type="type_2")
        }

    def add(self, model):
        """Simula agregar un nuevo tipo de tarjeta."""
        if model.id in self.typecards:
            raise ValueError("Type card ID already exists.")
        self.typecards[model.id] = TypeCardOut(id=model.id, type=model.type)
        return self.typecards[model.id]

    def update(self, model):
        """Simula la actualización de un tipo de tarjeta."""
        if model.id not in self.typecards:
            raise ValueError("Type card not found.")
        self.typecards[model.id] = TypeCardOut(id=model.id, type=model.type)
        return self.typecards[model.id]

    def delete(self, model):
        """Simula la eliminación de un tipo de tarjeta."""
        if model.id not in self.typecards:
            raise ValueError("Type card not found.")
        del self.typecards[model.id]
        return True

    def get_by_id(self, model, id_: int):
        """Simula la búsqueda de un tipo de tarjeta por ID."""
        return self.typecards.get(id_)

# Reemplazamos el controlador real por el mock
app.dependency_overrides[UniversalController] = MockUniversalController

# Inicializamos el cliente de pruebas de FastAPI
client = TestClient(app)

@pytest.fixture
def mock_controller():
    """Fixture para el mock del controlador"""
    return MockUniversalController()

def test_crear_tipo_tarjeta(mock_controller):
    """Prueba que la ruta '/typecard/create' crea correctamente un nuevo tipo de tarjeta."""
    response = client.post("/typecard/create", data={"id": 3, "type": "type_3"})
    assert response.status_code == 200
    data = response.json()
    assert data["operation"] == "create"
    assert data["success"] == True
    assert data["data"]["id"] == 3
    assert data["data"]["type"] == "type_3"

def test_crear_tipo_tarjeta_existing(mock_controller):
    """Prueba que la ruta '/typecard/create' devuelve un error cuando el ID de tarjeta ya existe."""
    response = client.post("/typecard/create", data={"id": 1, "type": "type_1"})
    assert response.status_code == 400
    assert "Type card ID already exists." in response.json()["detail"]

def test_actualizar_tipo_tarjeta(mock_controller):
    """Prueba que la ruta '/typecard/update' actualiza correctamente un tipo de tarjeta existente."""
    response = client.post("/typecard/update", data={"id": 1, "type": "updated_type_1"})
    assert response.status_code == 200
    data = response.json()
    assert data["operation"] == "update"
    assert data["success"] == True
    assert data["data"]["id"] == 1
    assert data["data"]["type"] == "updated_type_1"

def test_actualizar_tipo_tarjeta_not_found(mock_controller):
    """Prueba que la ruta '/typecard/update' devuelve un error si el tipo de tarjeta no se encuentra."""
    response = client.post("/typecard/update", data={"id": 999, "type": "new_type"})
    assert response.status_code == 404
    assert "Card type not found" in response.json()["detail"]

def test_eliminar_tipo_tarjeta(mock_controller):
    """Prueba que la ruta '/typecard/delete' elimina correctamente un tipo de tarjeta."""
    response = client.post("/typecard/delete", data={"id": 1})
    assert response.status_code == 200
    data = response.json()
    assert data["operation"] == "delete"
    assert data["success"] == True
    assert data["message"] == "Card type 1 deleted successfully"

def test_eliminar_tipo_tarjeta_not_found(mock_controller):
    """Prueba que la ruta '/typecard/delete' devuelve un error si el tipo de tarjeta no se encuentra."""
    response = client.post("/typecard/delete", data={"id": 999})
    assert response.status_code == 404
    assert "Card type not found" in response.json()["detail"]
