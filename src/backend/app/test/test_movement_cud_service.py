import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI, HTTPException

from src.backend.app.api.routes.movement_cud_service import app as movement_router
from src.backend.app.models.movement import MovementOut
from src.backend.app.logic.universal_controller_sql import UniversalController

# Creamos una instancia de FastAPI para montar el router
app = FastAPI()
app.include_router(movement_router)

# Mock de la clase UniversalController
class MockUniversalController:
    def __init__(self):
        self.movements = {
            1: MovementOut(id=1, type="income", amount=100.0),
            2: MovementOut(id=2, type="expense", amount=50.0),
        }

    def add(self, movement):
        self.movements[movement.id] = movement
        return movement  # Retornamos el objeto agregado

    def get_by_id(self, model, id_):
        return self.movements.get(id_)

    def update(self, movement):
        if movement.id in self.movements:
            self.movements[movement.id] = movement
            return movement  # Retornamos el objeto actualizado
        raise HTTPException(status_code=404, detail="Movement not found")

    def delete(self, movement):
        if movement.id in self.movements:
            del self.movements[movement.id]
            return movement  # Puedes devolver el eliminado o True
        raise HTTPException(status_code=404, detail="Movement not found")
# Inicializamos el cliente de pruebas
client = TestClient(app)

@pytest.fixture
def mock_controller():
    """Fixture para el mock del controlador"""
    return MockUniversalController()

def test_create_movement(mock_controller):
    """Prueba para crear un nuevo movimiento"""
    response = client.post("/movement/create", data={"id": 3, "type": "transfer", "amount": 150.0})
    assert response.status_code == 200
    data = response.json()
    assert data["operation"] == "create"
    assert data["success"] is True
    assert data["data"]["id"] == 3
    assert data["data"]["type"] == "transfer"
    assert data["data"]["amount"] == 150.0
    assert "Movement created successfully" in data["message"]

def test_update_existing_movement(mock_controller):
    """Prueba para actualizar un movimiento existente"""
    response = client.post("/movement/update", data={"id": 1, "type": "investment", "amount": 100.0})
    assert response.status_code == 200
    data = response.json()
    assert data["operation"] == "update"
    assert data["success"] is True
    assert data["data"]["id"] == 1
    assert data["data"]["type"] == "investment"
    assert "updated successfully" in data["message"]

def test_update_nonexistent_movement(mock_controller):
    """Prueba para intentar actualizar un movimiento que no existe"""
    response = client.post("/movement/update", data={"id": 999, "type": "investment", "amount": 100.0})
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Movement not found"

def test_delete_existing_movement(mock_controller):
    """Prueba para eliminar un movimiento existente"""
    response = client.post("/movement/delete", data={"id": 1})
    assert response.status_code == 200
    data = response.json()
    assert data["operation"] == "delete"
    assert data["success"] is True
    assert "deleted successfully" in data["message"]

def test_delete_nonexistent_movement(mock_controller):
    """Prueba para intentar eliminar un movimiento que no existe"""
    response = client.post("/movement/delete", data={"id": 999})
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Movement not found"
