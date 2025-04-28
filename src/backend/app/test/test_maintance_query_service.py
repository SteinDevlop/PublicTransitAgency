import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI
from src.backend.app.api.routes.maintance_query_service import router
from src.backend.app.logic.mantainment_controller import Controller

# Instancia de FastAPI
appp = FastAPI()

# Incluye el router en la aplicación
appp.include_router(router)

# Mock de la clase MaintainanceController
class MockMaintainanceController:
    def get_all(self):
        return [
            {"id": 1, "unit_id": 101, "status": "completed"},
            {"id": 2, "unit_id": 102, "status": "in-progress"}
        ]
    
    def get_by_id(self, id_: int):
        if id_ == 1:
            return {"id": 1, "unit_id": 101, "status": "completed"}
        elif id_ == 2:
            return {"id": 2, "unit_id": 102, "status": "in-progress"}
        return None

    def get_by_unit(self, unit_id: int):
        if unit_id == 101:
            return [{"id": 1, "unit_id": 101, "status": "completed"}]
        elif unit_id == 102:
            return [{"id": 2, "unit_id": 102, "status": "in-progress"}]
        return []

# Reemplazamos el controlador real por el mock en el objeto 'appp'
appp.dependency_overrides[Controller] = MockMaintainanceController

# Inicializamos el cliente de pruebas de FastAPI
client = TestClient(appp)

@pytest.fixture
def mock_controller():
    return MockMaintainanceController()

def test_get_all(mock_controller):
    response = client.get("/maintainance/maintainancements")
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]["status"] == "completed"

def test_get_by_id_existing():
    response = client.get("/maintainance/1")
    assert response.status_code == 200
    assert response.json()["status"] == "completed"
    
def test_get_by_id_not_found():
    response = client.get("/maintainance/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Not found"}

def test_get_by_unit():
    response = client.get("/maintainance/unit/101")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["unit_id"] == 101
    
    response_empty = client.get("/maintainance/unit/999")
    assert response_empty.status_code == 200
    assert len(response_empty.json()) == 0
