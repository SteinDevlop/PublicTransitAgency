import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI, HTTPException

from src.backend.app.api.routes.type_movement_cud_service import app as type_movement_router, get_controller
from src.backend.app.models.type_movement import TypeMovementOut
from src.backend.app.logic.universal_controller_sql import UniversalController

app = FastAPI()
app.include_router(type_movement_router)
client = TestClient(app)

# Mock del controlador
class MockUniversalController:
    def __init__(self):
        self.movements = {
            1: TypeMovementOut(id=1, type="income"),
            2: TypeMovementOut(id=2, type="expense"),
        }

    def add(self, movement):
        self.movements[movement.id] = movement
        return movement

    def get_by_id(self, model, id_):
        return self.movements.get(id_)

    def update(self, movement):
        if movement.id in self.movements:
            self.movements[movement.id] = movement
            return movement
        raise HTTPException(status_code=404, detail="Movement type not found")

    def delete(self, movement):
        if movement.id in self.movements:
            del self.movements[movement.id]
            return movement
        raise HTTPException(status_code=404, detail="Movement type not found")


@pytest.fixture
def mock_controller():
    return MockUniversalController()

@pytest.fixture(autouse=True)
def override_controller(mock_controller):
    app.dependency_overrides[get_controller] = lambda: mock_controller
    yield
    app.dependency_overrides.clear()

def test_create_movement():
    response = client.post("/movement/create", data={"id": 3, "type": "transfer"})
    assert response.status_code == 200
    data = response.json()
    assert data["operation"] == "create"
    assert data["success"] is True
    assert data["data"]["id"] == 3
    assert data["data"]["type"] == "transfer"
    assert "Movement type created successfully" in data["message"]

def test_update_existing_movement():
    response = client.post("/movement/update", data={"id": 1, "type": "investment"})
    assert response.status_code == 200
    data = response.json()
    assert data["operation"] == "update"
    assert data["success"] is True
    assert data["data"]["id"] == 1
    assert data["data"]["type"] == "investment"
    assert "Movement type updated successfully" in data["message"]

def test_update_nonexistent_movement():
    response = client.post("/movement/update", data={"id": 999, "type": "investment"})
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Movement type not found"

def test_delete_existing_movement():
    response = client.post("/movement/delete", data={"id": 1})
    assert response.status_code == 200
    data = response.json()
    assert data["operation"] == "delete"
    assert data["success"] is True
    assert "Movement type deleted successfully" in data["message"]

def test_delete_nonexistent_movement():
    response = client.post("/movement/delete", data={"id": 999})
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Movement type not found"
