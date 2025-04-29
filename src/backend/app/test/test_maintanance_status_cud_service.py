from fastapi.testclient import TestClient
from src.backend.app.api.routes.maintainance_status_cud_service import app

import pytest

client = TestClient(app)

@pytest.fixture
def valid_status_data():
    return {
        "id": 1,
        "unit": "Unidad 100",
        "type": "Preventivo",
        "status": "Completado"
    }

def test_create_status_json(valid_status_data):
    response = client.post(
        "/maintainance_status/create",
        data=valid_status_data,
        headers={"Accept": "application/json"}
    )
    assert response.status_code == 200
    resp_json = response.json()
    assert resp_json["success"] is True
    assert resp_json["operation"] == "create"
    assert "data" in resp_json
    assert "message" in resp_json

def test_create_status_html(valid_status_data):
    response = client.post(
        "/maintainance_status/create",
        data=valid_status_data,
        headers={"Accept": "text/html"}
    )
    assert response.status_code == 200
    assert "<html>" in response.text
    assert "Estado de Mantenimiento Creado" in response.text

def test_update_status_json(valid_status_data):
    response = client.post(
        "/maintainance_status/update",
        data=valid_status_data,
        headers={"Accept": "application/json"}
    )
    assert response.status_code == 200
    resp_json = response.json()
    assert resp_json["success"] is True
    assert resp_json["operation"] == "update"
    assert "data" in resp_json
    assert "message" in resp_json

def test_update_status_html(valid_status_data):
    response = client.post(
        "/maintainance_status/update",
        data=valid_status_data,
        headers={"Accept": "text/html"}
    )
    assert response.status_code == 200
    assert "<html>" in response.text
    assert "Estado Actualizado" in response.text

def test_delete_status_json():
    response = client.post(
        "/maintainance_status/delete",
        data={"id": 1},
        headers={"Accept": "application/json"}
    )
    assert response.status_code == 200
    resp_json = response.json()
    assert resp_json["success"] is True
    assert resp_json["operation"] == "delete" or "message" in resp_json

def test_delete_status_html():
    response = client.post(
        "/maintainance_status/delete",
        data={"id": 1},
        headers={"Accept": "text/html"}
    )
    assert response.status_code == 200
    assert "<html>" in response.text
    assert "Estado Eliminado" in response.text
