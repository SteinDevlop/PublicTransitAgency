"""import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI, HTTPException
from backend.app.logic.user_cud_service_postgre import app as user_router, get_controller
from backend.app.models.user import UserCreate

# Montar una app para test
test_app = FastAPI()
test_app.include_router(user_router)
client = TestClient(test_app)

# Mock para UniversalController
class MockUniversalController:
    def __init__(self):
        self.users = {
            1: UserCreate(
                id=1,
                identification=12345678,
                name="John",
                lastname="Doe",
                email="john@example.com",
                password="password@123",
                idtype_user=1,
                idturn=1
            ),
            2: UserCreate(
                id=2,
                identification=87654321,
                name="Jane",
                lastname="Doe",
                email="jane@example.com",
                password="password@123",
                idtype_user=2,
                idturn=2
            )
        }
        
    def add(self, user):
        self.users[user.id] = user
        return user

    def get_by_id(self, model, id_):
        return self.users.get(id_)

    def update(self, user):
        if user.id in self.users:
            self.users[user.id] = user
            return user
        raise HTTPException(status_code=404, detail="User not found")

    def delete(self, user):
        if user.id in self.users:
            del self.users[user.id]
            return user
        raise HTTPException(status_code=404, detail="User not found")

@pytest.fixture
def mock_controller():
    return MockUniversalController()

@pytest.fixture(autouse=True)
def override_controller(mock_controller):
    test_app.dependency_overrides[get_controller] = lambda: mock_controller
    yield
    test_app.dependency_overrides.clear()

def test_create_user():
    response = client.post("/user/create", data={"id": 3, "identification": 12345678, "name": "Alice", "lastname": "Smith", 
                        "email": "alice@example.com", "password": "password@123", "idtype_user": 1, "idturn": 1})
    assert response.status_code == 200
    data = response.json()
    assert data["operation"] == "create"
    assert data["success"] is True
    assert data["data"]["id"] == 3
    assert data["data"]["identification"] == 12345678
    assert data["data"]["name"] == "Alice"
    assert data["data"]["lastname"] == "Smith"
    assert data["data"]["email"] == "alice@example.com"
    assert data["data"]["password"] == "password@123"
    assert data["data"]["idtype_user"] == 1
    assert data["data"]["idturn"] == 1
    assert "User created successfully" in data["message"]

def test_update_existing_user():
    response = client.post("/user/update", data={"id": 1, "identification": 12345678, "name": "John", "lastname": "Doe",
                        "email": "doe@example.com", "password": "newpassword@123", "idtype_user": 1, "idturn": 1})
    assert response.status_code == 200
    data = response.json()
    assert data["operation"] == "update"
    assert data["success"] is True
    assert data["data"]["id"] == 1
    assert data["data"]["identification"] == 12345678
    assert data["data"]["name"] == "John"
    assert data["data"]["lastname"] == "Doe"
    assert data["data"]["email"] == "doe@example.com"
    assert data["data"]["password"] == "newpassword@123"
    assert data["data"]["idtype_user"] == 1
    assert data["data"]["idturn"] == 1
    assert "updated successfully" in data["message"]

def test_update_nonexistent_user():
    response = client.post("/user/update", data={"id": 999, "identification": 12345678, "name": "John", "lastname": "Doe",
                        "email": "john@example", "password": "newpassword@123", "idtype_user": 1, "idturn": 1})
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "User not found"

def test_delete_existing_user():
    response = client.post("/user/delete", data={"id": 1})
    assert response.status_code == 200
    data = response.json()
    assert data["operation"] == "delete"
    assert data["success"] is True
    assert "deleted successfully" in data["message"]

def test_delete_nonexistent_user():
    response = client.post("/user/delete", data={"id": 999})
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "User not found"
"""