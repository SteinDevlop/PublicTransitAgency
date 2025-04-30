import pytest
from fastapi.testclient import TestClient
from backend.app.api.main import app

client = TestClient(app)

# Datos de prueba
test_incidence = {
    "description": "Falla de motor",
    "type": "Mecánica",
    "status": "Abierta"
}

def test_create_incidence():
    response = client.post("/incidence/create", data=test_incidence)
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["description"] == test_incidence["description"]
    assert json_data["type"] == test_incidence["type"]
    assert json_data["status"] == test_incidence["status"]
    # Guardamos el ID generado para futuras pruebas
    test_incidence["incidence_id"] = json_data["incidence_id"]

def test_update_incidence():
    updated_data = test_incidence.copy()
    updated_data["description"] = "Falla eléctrica"
    response = client.post("/incidence/update", data=updated_data)
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["description"] == "Falla eléctrica"
    assert json_data["incidence_id"] == test_incidence["incidence_id"]

def test_delete_incidence():
    response = client.post("/incidence/delete", data={"incidence_id": test_incidence["incidence_id"]})
    assert response.status_code == 200
    assert f"Incidencia {test_incidence['incidence_id']} eliminada" in response.json()["message"]
