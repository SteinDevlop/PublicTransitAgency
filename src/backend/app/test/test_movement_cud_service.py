# test_movement_cud_service.py

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from backend.app.services.movement_cud_service import app as movement_router, get_controller
from .mock_controller import MockUniversalController

# Instancia de app para test
test_app = FastAPI()
test_app.include_router(movement_router)

# Override: cuando te pidan un controller, regresa el mock
test_app.dependency_overrides[get_controller] = lambda: MockUniversalController()

client = TestClient(test_app)

def test_create_movement():
    response = client.post("/movement/create", data={"id": 3, "type": "transfer", "amount": 150.0})
    assert response.status_code == 200
    assert response.json()["success"] == True

def test_update_existing_movement():
    response = client.post("/movement/update", data={"id": 1, "type": "investment", "amount": 100.0})
    assert response.status_code == 200
    assert response.json()["success"] == True
