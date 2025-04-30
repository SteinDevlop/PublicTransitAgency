from fastapi.testclient import TestClient
from fastapi import FastAPI
import pytest

from backend.app.api.main import api_router as app
from logic.universal_controller_sql import UniversalController
from backend.app.models.incidence import IncidenceOut

client = TestClient(app)

# Mock del UniversalController
class MockController:
    def __init__(self):
        self.data = {}
        self.next_id = 1

    def add(self, incidence):
        incidence_dict = incidence.dict()  # Convertir a diccionario
        incidence_dict["incidence_id"] = self.next_id
        self.data[self.next_id] = incidence_dict
        self.next_id += 1
        return IncidenceOut(**incidence_dict)  # Devolver instancia de IncidenceOut

    def get_by_id(self, model, incidence_id):
        if incidence_id in self.data:
            return IncidenceOut(**self.data[incidence_id])
        return None

    def update(self, incidence):
        incidence_dict = incidence.dict()
        if incidence_dict["incidence_id"] in self.data:
            self.data[incidence_dict["incidence_id"]] = incidence_dict
            return IncidenceOut(**incidence_dict)
        return None

    def delete(self, instance):
        if instance.incidence_id in self.data:
            del self.data[instance.incidence_id]
            return True
        return False

# Reemplaza el controlador real con el mock
@pytest.fixture(scope="function", autouse=True)
def override_controller():
    app.dependency_overrides[UniversalController] = lambda: MockController()
    yield
    app.dependency_overrides = {}

def test_create_incidence_success():
    response = client.post(
        "/incidence/create",
        data={
            "description": "Rueda pinchada",
            "type": "Mecánico",
            "status": "Pendiente",
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["description"] == "Rueda pinchada"
    assert body["type"] == "Mecánico"
    assert body["status"] == "Pendiente"
    assert body["incidence_id"] == 1

def test_create_incidence_invalid_data():
    response = client.post("/incidence/create", data={})
    assert response.status_code == 422

def test_update_incidence_success():
    # Primero crear una incidencia
    create_response = client.post(
        "/incidence/create",
        data={"description": "Viejo", "type": "Mecánico", "status": "Pendiente"},
    )
    assert create_response.status_code == 200
    incidence_id = create_response.json()["incidence_id"]

    # Luego actualizarla
    response = client.post(
        "/incidence/update",
        data={
            "incidence_id": incidence_id,
            "description": "Motor nuevo",
            "type": "Eléctrico",
            "status": "Resuelto",
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["incidence_id"] == incidence_id
    assert body["description"] == "Motor nuevo"
    assert body["type"] == "Eléctrico"
    assert body["status"] == "Resuelto"

def test_update_incidence_not_found():
    response = client.post(
        "/incidence/update",
        data={
            "incidence_id": 999,
            "description": "No existe",
            "type": "Desconocido",
            "status": "Inexistente",
        },
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Incidencia no encontrada"

def test_delete_incidence_success():
    # Primero crear una incidencia
    create_response = client.post(
        "/incidence/create",
        data={"description": "A eliminar", "type": "A eliminar", "status": "A eliminar"},
    )
    assert create_response.status_code == 200
    incidence_id = create_response.json()["incidence_id"]

    # Luego eliminarla
    response = client.post("/incidence/delete", data={"incidence_id": incidence_id})
    assert response.status_code == 200
    assert response.json()["message"] == f"Incidencia {incidence_id} eliminada correctamente"

def test_delete_incidence_not_found():
    response = client.post("/incidence/delete", data={"incidence_id": 999})
    assert response.status_code == 404
    assert response.json()["detail"] == "Incidencia no encontrada"