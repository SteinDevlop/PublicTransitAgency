"""
import pytest
from fastapi.testclient import TestClient
from backend.app.api.routes.rol_user_cud_service import app

client = TestClient(app)

@pytest.fixture
def mock_routes():
    return [
        {"route_id": "1", "route": "A-B-C"},
        {"route_id": "2", "route": "D-E-F"}
    ]

def test_create_route(mock_routes):
    route_data = {"route": "G-H-I", "route_id": "3"}
    
    with pytest.MonkeyPatch.context() as m:
        m.setattr("logic.universal_controller_sql.UniversalController.add", lambda self, data: route_data)
        
        response = client.post("/routes/create", json=route_data)
        assert response.status_code == 200
        assert response.json()["operation"] == "create"
        assert response.json()["message"] == "Ruta creada exitosamente"

def test_update_route(mock_routes):
    route_data = {"route": "A-B-C", "route_id": "1"}
    
    with pytest.MonkeyPatch.context() as m:
        m.setattr("logic.universal_controller_sql.UniversalController.get_by_id", lambda self, model, route_id: mock_routes[0] if route_id == "1" else None)
        m.setattr("logic.universal_controller_sql.UniversalController.update", lambda self, data: route_data)
        
        response = client.post("/routes/update", json=route_data)
        assert response.status_code == 200
        assert response.json()["operation"] == "update"
        assert response.json()["message"] == "Ruta 1 actualizada"

def test_delete_route(mock_routes):
    route_data = {"route_id": "1"}
    
    with pytest.MonkeyPatch.context() as m:
        m.setattr("logic.universal_controller_sql.UniversalController.get_by_id", lambda self, model, route_id: mock_routes[0] if route_id == "1" else None)
        m.setattr("logic.universal_controller_sql.UniversalController.delete", lambda self, data: None)
        
        response = client.post("/routes/delete", json=route_data)
        assert response.status_code == 200
        assert response.json()["operation"] == "delete"
        assert response.json()["message"] == "Ruta 1 eliminada"
"""