import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI, HTTPException

from backend.app.api.routes.type_transport_cud_service import app as type_transport_router, get_controller
from backend.app.models.type_transport import TypeTransportCreate, TypeTransportOut
from backend.app.logic.universal_controller_sql import UniversalController

app = FastAPI()
app.include_router(type_transport_router)
client = TestClient(app)

# Mock del controlador
class MockUniversalController:
    def __init__(self):
        self.transports = {
            1: TypeTransportOut(id=1, type="Bus"),
            2: TypeTransportOut(id=2, type="Boat"),
        }

    def add(self, transport):
        self.transports[transport.id] = transport
        return transport

    def get_by_id(self, model, id_):
        existing = self.transports.get(id_)
        if existing is not None:
            return existing
        if existing is None:
            raise HTTPException(404, detail="Not found")

    def update(self, transport):
        if transport.id in self.transports:
            self.transports[transport.id] = transport
            return transport
        raise HTTPException(status_code=404, detail="Not found")

    def delete(self, transport):
        if transport.id in self.transports:
            del self.transports[transport.id]
            return transport
        raise HTTPException(status_code=404, detail="Not found")


@pytest.fixture
def mock_controller():
    return MockUniversalController()

@pytest.fixture(autouse=True)
def override_controller(mock_controller):
    app.dependency_overrides[get_controller] = lambda: mock_controller
    yield
    app.dependency_overrides.clear()

def test_create_type_transport():
    response = client.post("/typetransport/create", data={"id": 3, "type": "train"})
    assert response.status_code == 200
    data = response.json()
    assert data["operation"] == "create"
    assert data["success"] is True
    assert data["data"]["id"] == 3
    assert data["data"]["type"] == "train"
    assert "Transport type created successfully" in data["message"]

def test_update_existing_type_transport():
    response = client.post("/typetransport/update", data={"id": 1, "type": "subway"})
    assert response.status_code == 200
    data = response.json()
    assert data["operation"] == "update"
    assert data["success"] is True
    assert data["data"]["id"] == 1
    assert data["data"]["type"] == "subway"
    assert "Transport type updated successfully" in data["message"]

def test_update_nonexistent_type_transport():
    response = client.post("/typetransport/update", data={"id": 999, "type": "unknown"})
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Not found"

def test_delete_existing_type_transport():
    response = client.post("/typetransport/delete", data={"id": 1})
    assert response.status_code == 200
    data = response.json()
    assert data["operation"] == "delete"
    assert data["success"] is True
    assert "Transport type deleted successfully" in data["message"]

def test_delete_nonexistent_type_transport():
    response = client.post("/typetransport/delete", data={"id": 999})
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Not found"
    