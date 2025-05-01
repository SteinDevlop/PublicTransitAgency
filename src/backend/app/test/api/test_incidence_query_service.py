import pytest
from fastapi.testclient import TestClient
from backend.app.api.routes.incidence_query_service import app as incidences_router
from backend.app.logic.universal_controller_sql import UniversalController
from backend.app.models.incidence import Incidence

client = TestClient(incidences_router)
<<<<<<< HEAD

def setup_function():
    """Limpia las tablas antes de cada prueba."""
    UniversalController().clear_tables()
=======


def setup_function():
    uc = UniversalController()
    uc.clear_tables()
    uc.add(Incidence(incidence_id=1, description="Accidente", type="Choque", status="Abierto"))

>>>>>>> 93460d8 (incidence fix)

def test_listar_incidencias():
    """Prueba la consulta de todas las incidencias."""
    controller = UniversalController()
    controller.add(Incidence(description="Accidente", status="Abierto", type="Choque"))
    response = client.get("/incidences/")
    assert response.status_code == 200
    assert "Accidente" in response.text
<<<<<<< HEAD

def test_detalle_incidencia_existente():
    """Prueba la consulta de una incidencia existente por ID."""
    controller = UniversalController()
    controller.add(Incidence(incidence_id=1, description="Accidente", status="Abierto", type="Choque"))
    response = client.get("/incidences/1")
    assert response.status_code == 200
    assert "Accidente" in response.text
=======
    assert "Choque" in response.text


def test_detalle_incidencia_existente():
    response = client.get("/incidences/1")
    assert response.status_code == 200
    assert "Accidente" in response.text
    assert "Choque" in response.text

>>>>>>> 93460d8 (incidence fix)

def test_detalle_incidencia_no_existente():
    """Prueba la consulta de una incidencia inexistente."""
    response = client.get("/incidences/999")
    assert response.status_code == 404
<<<<<<< HEAD
    assert "Incidencia no encontrada" in response.text
=======
    assert response.json()["detail"] == "Incidence not found"
>>>>>>> 93460d8 (incidence fix)
