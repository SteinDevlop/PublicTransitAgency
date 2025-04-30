"""
from fastapi.testclient import TestClient
from backend.app.api.routes.routes_query_service import app

client = TestClient(app)

def test_list_all_routes_success():
    response = client.get("/routes")
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["operation"] == "read_all"
    assert json_data["success"] is True
    assert isinstance(json_data["data"], list)
    assert "message" in json_data

def test_get_route_success():
    route_id = "test_route_id"  # Asegúrate que este ID exista en tu base de datos de prueba
    response = client.get(f"/routes/{route_id}")
    if response.status_code == 200:
        json_data = response.json()
        assert json_data["operation"] == "read_by_id"
        assert json_data["success"] is True
        assert isinstance(json_data["data"], dict)
        assert json_data["data"].get("route_id") == route_id
        assert "message" in json_data
    elif response.status_code == 404:
        json_data = response.json()
        assert json_data["detail"] == "Ruta no encontrada"
    else:
        assert False, f"Unexpected status code: {response.status_code}"

def test_get_route_not_found():
    non_existing_route_id = "non_existing_route"
    response = client.get(f"/routes/{non_existing_route_id}")
    assert response.status_code == 404
    json_data = response.json()
    assert json_data["detail"] == "Ruta no encontrada"
"""