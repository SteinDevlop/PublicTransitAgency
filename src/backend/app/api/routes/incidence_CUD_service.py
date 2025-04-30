"""
import pytest
from fastapi.testclient import TestClient
from backend.app.api.main import app

client = TestClient(app)

# Datos de prueba válidos
valid_incidence = {
    "description": "Falla de motor",
    "type": "Mecánica",
    "status": "Abierta"
}

# Guardar ID generado
incidence_id = None

def test_create_incidence_success():
    global incidence_id
    response = client.post("/incidence/create", data=valid_incidence)
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["description"] == valid_incidence["description"]
    assert json_data["type"] == valid_incidence["type"]
    assert json_data["status"] == valid_incidence["status"]
    incidence_id = json_data["incidence_id"]


def test_create_incidence_missing_fields():
    response = client.post("/incidence/create", data={"description": "Falla sin tipo"})
    assert response.status_code == 422  # Unprocessable Entity por validación faltante


def test_update_incidence_success():
    updated_data = {
        "incidence_id": incidence_id,
        "description": "Falla eléctrica actualizada",
        "type": "Eléctrica",
        "status": "En Proceso"
    }
    response = client.post("/incidence/update", data=updated_data)
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["description"] == "Falla eléctrica actualizada"
    assert json_data["type"] == "Eléctrica"
    assert json_data["status"] == "En Proceso"
    assert json_data["incidence_id"] == incidence_id


def test_update_incidence_invalid_id():
    response = client.post("/incidence/update", data={
        "incidence_id": "fake-id",
        "description": "Nada",
        "type": "Otro",
        "status": "Cerrada"
    })
    assert response.status_code in (404, 400)  # Según cómo manejes errores en backend


def test_delete_incidence_success():
    response = client.post("/incidence/delete", data={"incidence_id": incidence_id})
    assert response.status_code == 200
    assert f"Incidencia {incidence_id} eliminada" in response.json()["message"]


def test_delete_incidence_nonexistent():
    response = client.post("/incidence/delete", data={"incidence_id": "non-existent-id"})
    assert response.status_code in (404, 400)  # Según la implementación
"""