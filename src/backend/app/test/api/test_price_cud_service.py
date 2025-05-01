"""import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI, HTTPException
from src.backend.app.api.routes.price_cud_service import router as price_router, get_controller
from src.backend.app.models.price import PriceOut
from src.backend.app.logic.universal_controller_sql import UniversalController

app = FastAPI()
app.include_router(price_router)
client = TestClient(app)

# Mock del controlador
class MockUniversalController:
    def __init__(self):
        self.prices = {
            1: PriceOut(id=1, unidadtransportype="bus", amount=10.0),
            2: PriceOut(id=2, unidadtransportype="train", amount=20.0),
        }

    def add(self, price):
        self.prices[price.id] = price
        return price

    def get_by_id(self, model, id_):
        return self.prices.get(id_)

    def update(self, price):
        if price.id in self.prices:
            self.prices[price.id] = price
            return price
        raise HTTPException(status_code=404, detail="Price not found")

    def delete(self, price):
        if price.id in self.prices:
            del self.prices[price.id]
            return price
        raise HTTPException(status_code=404, detail="Price not found")

@pytest.fixture
def mock_controller():
    return MockUniversalController()

@pytest.fixture(autouse=True)
def override_controller(mock_controller):
    app.dependency_overrides[get_controller] = lambda: mock_controller
    yield
    app.dependency_overrides.clear()

def test_create_price():
    response = client.post("/price/create", data={"id": 3, "unidadtransportype": "metro", "amount": 15.0})
    assert response.status_code == 200
    data = response.json()
    assert data["operation"] == "create"
    assert data["success"] is True
    assert data["data"]["id"] == 3
    assert data["data"]["unidadtransportype"] == "metro"
    assert data["data"]["amount"] == 15.0
    assert "Price created successfully" in data["message"]

def test_update_existing_price():
    response = client.post("/price/update", data={"id": 1, "unidadtransportype": "taxi", "amount": 12.0})
    assert response.status_code == 200
    data = response.json()
    assert data["operation"] == "update"
    assert data["success"] is True
    assert data["data"]["id"] == 1
    assert data["data"]["unidadtransportype"] == "taxi"
    assert "updated successfully" in data["message"]

def test_update_nonexistent_price():
    response = client.post("/price/update", data={"id": 999, "unidadtransportype": "subway", "amount": 30.0})
    print(response.text)
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Price not found"

def test_delete_existing_price():
    response = client.post("/price/delete", data={"id": 1})
    assert response.status_code == 200
    data = response.json()
    assert data["operation"] == "delete"
    assert data["success"] is True
    assert "deleted successfully" in data["message"]

def test_delete_nonexistent_price():
    response = client.post("/price/delete", data={"id": 999})
    print(response.text)
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Price not found"
"""