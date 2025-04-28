import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from src.backend.app.models.type_card import TypeCardOut
from src.backend.app.api.routes.type_card_cud_service import app as typecard_router

# Preparamos una app de prueba
app_for_test = FastAPI()
app_for_test.include_router(typecard_router)

client = TestClient(app_for_test)

# Mock de UniversalController
class MockUniversalController:
    def __init__(self):
        self.data = {
            1: TypeCardOut(id=1, type="type_1"),
            2: TypeCardOut(id=2, type="type_2")
        }

    def add(self, model):
        if model.id in self.data:
            raise ValueError("Type card ID already exists.")
        self.data[model.id] = TypeCardOut(id=model.id, type=model.type)
        return self.data[model.id]

    def update(self, model):
        if model.id not in self.data:
            raise ValueError("Card type not found")
        self.data[model.id] = TypeCardOut(id=model.id, type=model.type)
        return self.data[model.id]

    def delete(self, model):
        if isinstance(model, dict):
            id_ = model["id"]
        else:
            id_ = model.id
        
        if id_ not in self.data:
            raise ValueError("Card type not found")
        del self.data[id_]
        return True

    def get_by_id(self, model, id):
        return self.data.get(id)

# Fixture para reemplazar el controller real por el mock
@pytest.fixture(autouse=True)
def override_controller(monkeypatch):
    from src.backend.app.api.routes import type_card_cud_service
    type_card_cud_service.controller = MockUniversalController()

# Ahora los tests:

def test_create_typecard_success():
    response = client.post("/typecard/create", data={"id": 3, "type": "type_3"})
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["operation"] == "create"
    assert json_data["success"] == True
    assert json_data["data"]["id"] == 3
    assert json_data["data"]["type"] == "type_3"

def test_create_typecard_already_exists():
    response = client.post("/typecard/create", data={"id": 1, "type": "type_1"})
    assert response.status_code == 400
    assert "Type card ID already exists." in response.json()["detail"]

def test_update_typecard_success():
    response = client.post("/typecard/update", data={"id": 1, "type": "updated_type_1"})
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["operation"] == "update"
    assert json_data["success"] == True
    assert json_data["data"]["id"] == 1
    assert json_data["data"]["type"] == "updated_type_1"

def test_update_typecard_not_found():
    response = client.post("/typecard/update", data={"id": 999, "type": "nonexistent"})
    assert response.status_code == 404
    assert "Card type not found" in response.json()["detail"]

def test_delete_typecard_success():
    response = client.post("/typecard/delete", data={"id": 2})
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["operation"] == "delete"
    assert json_data["success"] == True
    assert "deleted successfully" in json_data["message"]

def test_delete_typecard_not_found():
    response = client.post("/typecard/delete", data={"id": 999})
    assert response.status_code == 404
    assert "Card type not found" in response.json()["detail"]
