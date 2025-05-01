"""import pytest
from fastapi.testclient import TestClient
from backend.app.api.routes.incidence_query_service import app as incidences_router
from backend.app.logic.universal_controller_sql import UniversalController
from backend.app.models.incidence import Incidence

client = TestClient(incidences_router)

def setup_function():
    |||Limpia las tablas antes de cada prueba.|||
    UniversalController().clear_tables()

def test_listar_incidencias():
    response = client.get("/incidences/")
    assert response.status_code == 200

def test_detalle_incidencia_existente():
    controller = UniversalController()
    controller.add(Incidence(incidence_id=1, description="Accidente", type="Choque", status="Abierto"))
    response = client.get("/incidences/1")
    assert response.status_code == 200

def test_detalle_incidencia_no_existente():
    response = client.get("/incidences/999")
    assert response.status_code == 404
"""