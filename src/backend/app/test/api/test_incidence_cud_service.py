import pytest
from fastapi.testclient import TestClient
from backend.app.api.routes.incidence_cud_service import app as incidences_router
from backend.app.logic.universal_controller_sql import UniversalController
from backend.app.models.incidence import Incidence

client = TestClient(incidences_router)

def setup_function():
    UniversalController().clear_tables()

def test_crear_incidencia():
    response = client.post("/incidence/create", data={"description": "Accidente", "type": "Choque", "status": "Abierto"})
    assert response.status_code == 303

def test_actualizar_incidencia():
    controller = UniversalController()
    controller.add(Incidence(incidence_id=1, description="Accidente", type="Choque", status="Abierto"))
    response = client.post("/incidence/update", data={"incidence_id": 1, "description": "Actualizado", "type": "Choque", "status": "Cerrado"})
    assert response.status_code == 303

def test_eliminar_incidencia():
    controller = UniversalController()
    controller.add(Incidence(incidence_id=1, description="Accidente", type="Choque", status="Abierto"))
    response = client.post("/incidence/delete", data={"incidence_id": 1})
    assert response.status_code == 303