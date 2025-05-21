import pytest
from fastapi import FastAPI, status
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from backend.app.api.routes.pqr_service.pqr_cud_service import router as pqr_router

app = FastAPI()
app.include_router(pqr_router)
client = TestClient(app)

@pytest.fixture
def pqr_data():
    return {
        "ID": 1,
        "type": "t",
        "description": "d",
        "fecha": "2024-01-01",
        "identificationuser": 9
    }

def test_index_create_admin_success():
    with patch("backend.app.logic.universal_controller_instance.universal_controller.read_all", return_value=[{"ID": 1}, {"ID": 2}]):
        response = client.get("/pqr/administrador/crear")
        assert response.status_code == 200
        assert response.json()["nuevo_id"] == 3

def test_index_create_admin_empty():
    with patch("backend.app.logic.universal_controller_instance.universal_controller.read_all", return_value=[]):
        response = client.get("/pqr/administrador/crear")
        assert response.status_code == 200
        assert response.json()["nuevo_id"] == 1

def test_index_create_admin_exception():
    with patch("backend.app.logic.universal_controller_instance.universal_controller.read_all", side_effect=Exception("fail")):
        response = client.get("/pqr/administrador/crear")
        assert response.status_code == 200
        assert response.json()["nuevo_id"] == 1

def test_index_create_pasajero_success():
    with patch("backend.app.logic.universal_controller_instance.universal_controller.read_all", return_value=[{"ID": 5}]):
        response = client.get("/pqr/pasajero/crear")
        assert response.status_code == 200
        assert response.json()["nuevo_id"] == 6

def test_index_update_admin():
    response = client.get("/pqr/administrador/actualizar")
    assert response.status_code == 200
    assert "message" in response.json()

def test_index_delete_admin():
    response = client.get("/pqr/administrador/eliminar")
    assert response.status_code == 200
    assert "message" in response.json()

def test_create_pqr_success(pqr_data):
    with patch("backend.app.logic.universal_controller_instance.universal_controller.get_by_column", return_value=None), \
         patch("backend.app.logic.universal_controller_instance.universal_controller.add"):
        response = client.post("/pqr/create", data=pqr_data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["success"] is True

def test_create_pqr_duplicate(pqr_data):
    with patch("backend.app.logic.universal_controller_instance.universal_controller.get_by_column", return_value=MagicMock()):
        response = client.post("/pqr/create", data=pqr_data)
        assert response.status_code == 500
        assert "ya existe" in response.json()["detail"]

def test_create_pqr_valueerror(pqr_data):
    with patch("backend.app.logic.universal_controller_instance.universal_controller.get_by_column", return_value=None), \
         patch("backend.app.logic.universal_controller_instance.universal_controller.add", side_effect=ValueError("Fallo val")):
        response = client.post("/pqr/create", data=pqr_data)
        assert response.status_code == 400
        assert "Fallo val" in response.json()["detail"]

def test_create_pqr_exception(pqr_data):
    with patch("backend.app.logic.universal_controller_instance.universal_controller.get_by_column", return_value=None), \
         patch("backend.app.logic.universal_controller_instance.universal_controller.add", side_effect=Exception("GRAVE")):
        response = client.post("/pqr/create", data=pqr_data)
        assert response.status_code == 500
        assert "Internal server error" in response.json()["detail"]

def test_update_pqr_success(pqr_data):
    with patch("backend.app.logic.universal_controller_instance.universal_controller.get_by_column", return_value=MagicMock()), \
         patch("backend.app.logic.universal_controller_instance.universal_controller.update"):
        response = client.post("/pqr/update", data=pqr_data)
        assert response.status_code == 200
        assert response.json()["success"]

def test_update_pqr_not_found(pqr_data):
    with patch("backend.app.logic.universal_controller_instance.universal_controller.get_by_column", return_value=None):
        response = client.post("/pqr/update", data=pqr_data)
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]

def test_update_pqr_valueerror(pqr_data):
    with patch("backend.app.logic.universal_controller_instance.universal_controller.get_by_column", return_value=MagicMock()), \
         patch("backend.app.logic.universal_controller_instance.universal_controller.update", side_effect=ValueError("fallo update")):
        response = client.post("/pqr/update", data=pqr_data)
        assert response.status_code == 400
        assert "fallo update" in response.json()["detail"]

def test_delete_pqr_success(pqr_data):
    with patch("backend.app.logic.universal_controller_instance.universal_controller.get_by_column", return_value=MagicMock()), \
         patch("backend.app.logic.universal_controller_instance.universal_controller.delete"):
        response = client.post("/pqr/delete", data={"ID": pqr_data["ID"]})
        assert response.status_code == 200
        assert response.json()["success"]

def test_delete_pqr_not_found(pqr_data):
    with patch("backend.app.logic.universal_controller_instance.universal_controller.get_by_column", return_value=None):
        response = client.post("/pqr/delete", data={"ID": pqr_data["ID"]})
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]

def test_delete_pqr_exception(pqr_data):
    with patch("backend.app.logic.universal_controller_instance.universal_controller.get_by_column", return_value=MagicMock()), \
         patch("backend.app.logic.universal_controller_instance.universal_controller.delete", side_effect=Exception("fallo grave")):
        response = client.post("/pqr/delete", data={"ID": pqr_data["ID"]})
        assert response.status_code == 500
        assert "Internal server error" in response.json()["detail"]

# Tests de campos inválidos/extremos:
@pytest.mark.parametrize("field,value", [
    ("ID", ""),
    ("type", ""),
    ("description", ""),
    ("fecha", ""),
    ("identificationuser", ""),
])
def test_create_pqr_invalid_fields(field, value, pqr_data):
    data = pqr_data.copy()
    data[field] = value
    response = client.post("/pqr/create", data=data)
    assert response.status_code in (422, 400)