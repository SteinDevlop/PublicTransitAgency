import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI, HTTPException
from backend.app.api.routes.movement_cud_service import app as movement_router, get_controller
from backend.app.models.movement import MovementOut
from backend.app.logic.universal_controller_sql import UniversalController

app = FastAPI()
app.include_router(movement_router)
client = TestClient(app)

# Mock del controlador
class MockUniversalController:
    def __init__(self):
        self.movements = {
            1: MovementOut(id=1, type="income", amount=100.0),
            2: MovementOut(id=2, type="expense", amount=50.0),
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
        raise HTTPException(status_code=404, detail="Movement not found")

    def delete(self, movement):
        if movement.id in self.movements:
            del self.movements[movement.id]
            return movement
        raise HTTPException(status_code=404, detail="Movement not found")


@pytest.fixture
def mock_controller():
    return MockUniversalController()

@pytest.fixture(autouse=True)
def override_controller(mock_controller):
    app.dependency_overrides[get_controller] = lambda: mock_controller
    yield
    app.dependency_overrides.clear()

def test_create_movement():
    response = client.post("/movement/create", data={"id": 3, "type": "transfer", "amount": 150.0})
    assert response.status_code == 200
    data = response.json()
    assert data["operation"] == "create"
    assert data["success"] is True
    assert data["data"]["id"] == 3
    assert data["data"]["type"] == "transfer"
    assert data["data"]["amount"] == 150.0
    assert "Movement created successfully" in data["message"]

def test_update_existing_movement():
    response = client.post("/movement/update", data={"id": 1, "type": "investment", "amount": 100.0})
    assert response.status_code == 200
    data = response.json()
    assert data["operation"] == "update"
    assert data["success"] is True
    assert data["data"]["id"] == 1
    assert data["data"]["type"] == "investment"
    assert "updated successfully" in data["message"]

def test_update_nonexistent_movement():
    response = client.post("/movement/update", data={"id": 999, "type": "investment", "amount": 100.0})
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Movement not found"

def test_delete_existing_movement():
    response = client.post("/movement/delete", data={"id": 1})
    assert response.status_code == 200
    data = response.json()
    assert data["operation"] == "delete"
    assert data["success"] is True
    assert "deleted successfully" in data["message"]

def test_delete_nonexistent_movement():
    response = client.post("/movement/delete", data={"id": 999})
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Movement not found"
