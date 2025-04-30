from fastapi.testclient import TestClient
from fastapi import FastAPI, HTTPException
import pytest
from unittest.mock import MagicMock

from backend.app.api.main import api_router as app
from logic.universal_controller_sql import UniversalController
from backend.app.models.incidence import IncidenceCreate, IncidenceOut


client = TestClient(app)


# Mock del UniversalController
class MockController:
    def __init__(self):
        self.data = {}
        self.next_id = 1

    def add(self, incidence):
        incidence_dict = incidence.dict()
        if "incidence_id" not in incidence_dict or incidence_dict["incidence_id"] is None:
            incidence_dict["incidence_id"] = self.next_id
            self.next_id += 1
        self.data[incidence_dict["incidence_id"]] = incidence_dict
        return IncidenceOut(**incidence_dict)

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


# Tests para los endpoints GET (formularios HTML)
def test_show_create_form():
    response = client.get("/incidence/crear")
    assert response.status_code == 200
    assert "CrearIncidencia.html" in response.text


def test_show_update_form():
    response = client.get("/incidence/actualizar")
    assert response.status_code == 200
    assert "ActualizarIncidencia.html" in response.text


def test_show_delete_form():
    response = client.get("/incidence/eliminar")
    assert response.status_code == 200
    assert "EliminarIncidencia.html" in response.text


# Tests para el endpoint /incidence/create (POST)
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
    assert response.status_code == 422  # Unprocessable Entity
    assert "detail" in response.json()  # Asegurarse de que los detalles del error están presentes



def test_create_incidence_value_error():
    # Mock para simular un ValueError en el controlador
    mock_controller = MagicMock()
    mock_controller.add.side_effect = ValueError("Error de valor en la creación")
    app.dependency_overrides[UniversalController] = lambda: mock_controller

    response = client.post(
        "/incidence/create",
        data={
            "description": "Descripción",
            "type": "Tipo",
            "status": "Estado",
        },
    )
    assert response.status_code == 400
    assert "detail" in response.json()
    assert "Error de valor en la creación" in response.json()["detail"]
    app.dependency_overrides = {}  # Limpiar el override



# Tests para el endpoint /incidence/update (POST)
def test_update_incidence_success():
    # Primero crear una incidencia para poder actualizarla
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
    assert "detail" in response.json()
    assert response.json()["detail"] == "Incidencia no encontrada"



def test_update_incidence_value_error():
    # Mock para simular un ValueError en el controlador
    mock_controller = MagicMock()
    mock_controller.update.side_effect = ValueError("Error de valor al actualizar")
    app.dependency_overrides[UniversalController] = lambda: mock_controller

    # Primero crear una incidencia para poder actualizarla
    create_response = client.post(
        "/incidence/create",
        data={"description": "Viejo", "type": "Mecánico", "status": "Pendiente"},
    )
    assert create_response.status_code == 200
    incidence_id = create_response.json()["incidence_id"]

    response = client.post(
        "/incidence/update",
        data={
            "incidence_id": incidence_id,
            "description": "Motor nuevo",
            "type": "Eléctrico",
            "status": "Resuelto",
        },
    )
    assert response.status_code == 400
    assert "detail" in response.json()
    assert "Error de valor al actualizar" in response.json()["detail"]
    app.dependency_overrides = {}  # Limpiar el override



# Tests para el endpoint /incidence/delete (POST)
def test_delete_incidence_success():
    # Primero crear una incidencia
    create_response = client.post(
        "/incidence/create",
        data={"description": "A eliminar", "type": "A eliminar", "status": "Pendiente"},
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
    assert "detail" in response.json()
    assert response.json()["detail"] == "Incidencia no encontrada"



def test_delete_incidence_error():
    # Mock para simular un error genérico en el controlador
    mock_controller = MagicMock()
    mock_controller.delete.side_effect = Exception("Error genérico al eliminar")
    app.dependency_overrides[UniversalController] = lambda: mock_controller

    # Primero crear una incidencia
    create_response = client.post(
        "/incidence/create",
        data={"description": "A eliminar", "type": "A eliminar", "status": "Pendiente"},
    )
    assert create_response.status_code == 200
    incidence_id = create_response.json()["incidence_id"]

    response = client.post("/incidence/delete", data={"incidence_id": incidence_id})
    assert response.status_code == 500  # Internal Server Error
    assert "detail" in response.json()
    assert "Error genérico al eliminar" in response.json()["detail"]
    app.dependency_overrides = {}  # Limpiar el override
