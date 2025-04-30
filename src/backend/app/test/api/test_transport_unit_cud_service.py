import pytest
from fastapi.testclient import TestClient
from backend.app.api.routes.transport_unit_CUD_service import app
#Mario, esto es una correccion rapida, si tiene error te toca corregirlo
client = TestClient(app)

def test_create_unit():
    response = client.post(
        "/transport/unit/create",
        data={
            "id": "unit123",
            "type": "bus",
            "status": "active",
            "ubication": "warehouse_1",
            "capacity": 50
        }
    )
    assert response.status_code == 200
    assert response.json()["operation"] == "create"
    assert "data" in response.json()

def test_update_unit():
    response = client.post(
        "/transport/unit/update",
        data={
            "id": "unit123",
            "type": "bus",
            "status": "inactive",
            "ubication": "warehouse_2",
            "capacity": 40
        }
    )
    assert response.status_code == 200
    assert response.json()["operation"] == "update"
    assert response.json()["id"] == "unit123"

def test_delete_unit():
    response = client.post(
        "/transport/unit/delete",
        data={
            "id": "unit123"
        }
    )
    assert response.status_code == 200
    assert response.json()["operation"] == "delete"
    assert response.json()["id"] == "unit123"

def test_create_unit_missing_field():
    response = client.post(
        "/transport/unit/create",
        data={
            "id": "unit123",
            "type": "bus",
            "status": "active",
            "ubication": "warehouse_1"
        }
    )
    assert response.status_code == 422  
