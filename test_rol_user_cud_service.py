import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI, HTTPException

from src.backend.app.api.routes.rol_user_cud_service import app as rol_user_router, get_controller
from src.backend.app.models.rol_user import RolUserCreate, RolUserOut
from src.backend.app.logic.universal_controller_sql import UniversalController

app = FastAPI()
app.include_router(rol_user_router)
client = TestClient(app)

# Mock del controlador
class MockUniversalController:
    def __init__(self):
        self.users = {
            1: RolUserOut(id=1, type="passanger"),
            2: RolUserOut(id=2, type="driver"),
        }

    def add(self, user):
        self.users[user.id] = user
        return user

    def get_by_id(self, model, id_):
        existing = self.users.get(id_)
        if existing is not None:
            return existing
        if existing is None:
            raise HTTPException(404, detail="User Role not found")

    def update(self, user):
        if user.id in self.users:
            self.users[user.id] = user
            return user
        raise HTTPException(status_code=404, detail="User Role not found")

    def delete(self, user):
        if user.id in self.users:
            del self.users[user.id]
            return user
        raise HTTPException(status_code=404, detail="User Role not found")


@pytest.fixture
def mock_controller():
    return MockUniversalController()

@pytest.fixture(autouse=True)
def override_controller(mock_controller):
    app.dependency_overrides[get_controller] = lambda: mock_controller
    yield
    app.dependency_overrides.clear()

def test_create_user():
    response = client.post("/roluser/create", data={"id": 3, "type": "admin"})
    assert response.status_code == 200
    data = response.json()
    assert data["operation"] == "create"
    assert data["success"] is True
    assert data["data"]["id"] == 3
    assert data["data"]["type"] == "admin"
    assert "User Role created successfully" in data["message"]

def test_update_existing_user():
    response = client.post("/typeuser/update", data={"id": 1, "type": "maintenance"})
    assert response.status_code == 200
    data = response.json()
    assert data["operation"] == "update"
    assert data["success"] is True
    assert data["data"]["id"] == 1
    assert data["data"]["type"] == "passanger"
    assert "User Role updated successfully" in data["message"]

def test_update_nonexistent_user():
    response = client.post("/typeuser/update", data={"id": 999, "type": "admin"})
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "User Role not found"

def test_delete_existing_user():
    response = client.post("/typeuser/delete", data={"id": 1})
    assert response.status_code == 200
    data = response.json()
    assert data["operation"] == "delete"
    assert data["success"] is True
    assert "User Role deleted successfully" in data["message"]

def test_delete_nonexistent_user():
    response = client.post("/typeuser/delete", data={"id": 999})
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "User Role not found"