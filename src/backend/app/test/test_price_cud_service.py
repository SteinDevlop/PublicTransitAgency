import pytest
from fastapi import FastAPI, HTTPException, Depends
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from backend.app.models.price import PriceCreate, PriceOut
from src.backend.app.api.routes.price_cud_service import app as price_router, get_controller  # Ajusta si el archivo se llama diferente
from src.backend.app.logic.universal_controller_sql import UniversalController

# Setup FastAPI app para pruebas
app = FastAPI()
app.include_router(price_router)
client = TestClient(app)

# Fixture que simula el controlador con funciones básicas mockeadas
# Mock del controlador
class MockUniversalController:
    def __init__(self):
        self.prices = {
            1: PriceOut(id=1, unidadtransportype="Train", amount=100.0),
            2: PriceOut(id=2, unidadtransportype="Bus", amount=50.0),
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

# Test de creación
def test_create_price():
    response = client.post("/price/create", data={
        "id": 3,
        "unidadtransportype": "Boat",
        "amount": 3000.0
    })
    assert response.status_code == 200
    result = response.json()
    assert result["operation"] == "create"
    assert result["success"] is True
    assert result["data"]["unidadtransportype"] == "Boat"

# Test de actualización (cuando existe el ID)
def test_update_price_success():
    response = client.post("/price/update", data={
        "id": 1,
        "unidadtransportype": "Plane",
        "amount": 9999.0  # Este valor se ignora en lógica actual
    })
    assert response.status_code == 200
    result = response.json()
    assert result["operation"] == "update"
    assert result["success"] is True
    assert result["data"]["unidadtransportype"] == "Plane"

# Test de actualización fallida (ID no encontrado)
def test_update_price_not_found():
    response = client.post("/price/update", data={
        "id": 999,
        "unidadtransportype": "Boat",
        "amount": 4000.0
    })
    assert response.status_code == 404
    assert response.json()["detail"] == "price not found"

# Test de eliminación (cuando existe)
def test_delete_price_success():
    response = client.post("/price/delete", data={"id": 1})
    assert response.status_code == 200
    assert response.json()["operation"] == "delete"

# Test de eliminación fallida (ID no encontrado)
def test_delete_price_not_found():
    response = client.post("/price/delete", data={"id": 999})
    assert response.status_code == 404
    assert response.json()["detail"] == "Price not found"
