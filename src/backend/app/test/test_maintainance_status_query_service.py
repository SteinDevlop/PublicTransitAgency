"""from fastapi.testclient import TestClient
from backend.app.api.routes.maintainance_status_query_service import app
from models.maintainance_status import MaintainanceStatusOut

client = TestClient(app)

def test_get_all_maintainance_status():
    response = client.get("/maintainance_status/all")
    assert response.status_code == 200
    assert "data" in response.json()

def test_get_maintainance_status_not_found():
    response = client.get("/maintainance_status/999")  
    assert response.status_code == 404
    assert "Estado de mantenimiento no encontrado" in response.text

def test_get_maintainance_status():
    response = client.get("/maintainance_status/1")  
    assert response.status_code == 200
    assert "data" in response.json()
    assert response.json()["data"]["id"] == 1 
"""