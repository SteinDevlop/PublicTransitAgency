import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from fastapi.staticfiles import StaticFiles
from backend.app.models.type_card import TypeCardOut
from backend.app.api.routes.type_card_service.type_card_cud_service import app as typecard_router
from backend.app.logic.universal_controller_sql import UniversalController
from backend.app.core.conf import headers
def setup_function():
    UniversalController().clear_tables()

def teardown_function():
    UniversalController().clear_tables()
# Preparamos una app de prueba
app_for_test = FastAPI()
app_for_test.include_router(typecard_router)

client = TestClient(app_for_test)
app_for_test.mount("/static", StaticFiles(directory="src/frontend/static"), name="static")
# Mock de UniversalController
class MockUniversalController:
    def __init__(self):
        self.data = {
            1: TypeCardOut(ID=1, Tipo="type_1"),
            2: TypeCardOut(ID=2, Tipo="type_2")
        }

    def add(self, model):
        if model.ID in self.data:
            raise ValueError("Type card ID already exists.")
        self.data[model.ID] = TypeCardOut(ID=model.ID, Tipo=model.Tipo)
        return self.data[model.ID]

    def update(self, model):
        if model.ID not in self.data:
            raise ValueError("Card Tipo not found")
        self.data[model.ID] = TypeCardOut(ID=model.ID, Tipo=model.Tipo)
        return self.data[model.ID]

    def delete(self, model):
        if isinstance(model, dict):
            id_ = model["ID"]
        else:
            id_ = model.ID
        
        if id_ not in self.data:
            raise ValueError("Card Tipo not found")
        del self.data[id_]
        return True

    def get_by_id(self, model, ID):
        return self.data.get(ID)

# Fixture para reemplazar el controller real por el mock
@pytest.fixture(autouse=True)
def override_controller(monkeypatch):
    from backend.app.api.routes.type_card_service import type_card_cud_service
    type_card_cud_service.controller = MockUniversalController()

# Ahora los tests:

def test_create_typecard_success():
    response = client.post("/typecard/create", data={"ID": 3, "Tipo": "type_3"},headers=headers)
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["operation"] == "create"
    assert json_data["success"] == True
    assert json_data["data"]["ID"] == 3
    assert json_data["data"]["Tipo"] == "type_3"

def test_create_typecard_already_exists():
    response = client.post("/typecard/create", data={"ID": 1, "Tipo": "type_1"},headers=headers)
    assert response.status_code == 400
    assert "Type card ID already exists." in response.json()["detail"]

def test_update_typecard_success():
    response = client.post("/typecard/update", data={"ID": 1, "Tipo": "updated_type_1"},headers=headers)
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["operation"] == "update"
    assert json_data["success"] == True
    assert json_data["data"]["ID"] == 1
    assert json_data["data"]["Tipo"] == "updated_type_1"

def test_update_typecard_not_found():
    response = client.post("/typecard/update", data={"ID": 999, "Tipo": "nonexistent"},headers=headers)
    assert response.status_code == 404
    assert "Card Tipo not found" in response.json()["detail"]

def test_delete_typecard_success():
    response = client.post("/typecard/delete", data={"ID": 2},headers=headers)
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["operation"] == "delete"
    assert json_data["success"] == True
    assert "deleted successfully" in json_data["message"]

def test_delete_typecard_not_found():
    response = client.post("/typecard/delete", data={"ID": 999},headers=headers)
    assert response.status_code == 404
    assert "Card Tipo not found" in response.json()["detail"]
