from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest import mock
import pytest
from backend.app.api.routes.incidence_query_service import app as incidence_query_router
from backend.app.models.incidence import IncidenceOut

# Creamos la app de prueba
@pytest.fixture
def app():
    app = FastAPI()
    app.include_router(incidence_query_router)
    return app

@pytest.fixture
def client(app):
    return TestClient(app)

@pytest.fixture
def mock_controller():
    with mock.patch("backend.app.api.routes.incidence_query_service.UniversalController") as MockController:
        mock_controller_instance = MockController.return_value
        yield mock_controller_instance

# Datos de prueba mockeados
test_incidences_data = [
    {"incidence_id": 1, "description": "Fallo A", "type": "Crítico", "status": "activo"},
    {"incidence_id": 2, "description": "Problema B", "type": "Medio", "status": "pendiente"},
    {"incidence_id": 3, "description": "Error C", "type": "Bajo", "status": "activo"},
    {"incidence_id": 4, "description": "Solicitud D", "type": "Medio", "status": "completado"},
    {"incidence_id": 5, "description": "Fallo E", "type": "Crítico", "status": "activo"},
]
test_incidences = [IncidenceOut(**data) for data in test_incidences_data]

def test_listar_incidencias_html_sin_filtros(client, mock_controller):
    mock_controller.read_all.return_value = test_incidences
    response = client.get("/incidences")
    assert response.status_code == 200
    assert "Fallo A" in response.text
    assert "Problema B" in response.text
    mock_controller.read_all.assert_called_once()

def test_listar_incidencias_html_con_filtro(client, mock_controller):
    mock_controller.read_all.return_value = [i for i in test_incidences if i.status == "activo"]
    response = client.get("/incidences?status=activo")
    assert response.status_code == 200
    assert "Fallo A" in response.text
    assert "Problema B" not in response.text
    assert "Error C" in response.text
    mock_controller.read_all.assert_called_once()


def test_listar_incidencias_json_sin_filtros(client, mock_controller):
    mock_controller.read_all.return_value = test_incidences
    response = client.get("/incidences/json")
    assert response.status_code == 200
    assert len(response.json()["data"]) == 5
    mock_controller.read_all.assert_called_once()



def test_obtener_incidencia_html_existente(client, mock_controller):
    mock_controller.get_by_id.return_value = test_incidences[0]
    response = client.get("/incidences/1")
    assert response.status_code == 200
    assert "Fallo A" in response.text
    mock_controller.get_by_id.assert_called_once_with(IncidenceOut, 1)


def test_obtener_incidencia_json_existente(client, mock_controller):
    mock_controller.get_by_id.return_value = test_incidences[0]
    response = client.get("/incidences/1/json")
    assert response.status_code == 200
    assert response.json()["data"]["description"] == "Fallo A"
    mock_controller.get_by_id.assert_called_once_with(IncidenceOut, 1)


def test_consultar_incidencias_form(client):
    response = client.get("/incidences/consultar")
    assert response.status_code == 200
    assert "ConsultarIncidencia" in response.text