from fastapi import FastAPI
from fastapi.testclient import TestClient
from backend.app.api.routes.maintainance_status_query_service import app as maintainance_router
from backend.app.logic.universal_controller_sql import UniversalController
from backend.app.models.maintainance_status import MaintainanceStatus

client = TestClient(maintainance_router)

def setup_function():
    """Limpia las tablas antes de cada prueba."""
    UniversalController().clear_tables()

def teardown_function():
    """Limpia las tablas después de cada prueba."""
    UniversalController().clear_tables()

def test_get_all_status():
    """Prueba que la ruta '/' devuelve correctamente todos los estados de mantenimiento."""
    # Crear algunos estados de mantenimiento
    controller = UniversalController()
    controller.add(MaintainanceStatus(status="No hecho"))
    controller.add(MaintainanceStatus(status="En progreso"))

    response = client.get("/maintainance-status/")
    assert response.status_code == 200
    assert "No hecho" in response.text
    assert "En progreso" in response.text

def test_get_status_by_id_existing():
    """Prueba que la ruta '/{id}' devuelve el estado correcto cuando existe."""
    # Crear un estado de mantenimiento
    controller = UniversalController()
    created = controller.add(MaintainanceStatus(status="Hecho"))
    status_id = created["id"]

    response = client.get(f"/maintainance-status/{status_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "Hecho"

def test_get_status_by_id_not_found():
    """Prueba que la ruta '/{id}' devuelve un error 404 cuando no encuentra el estado."""
    response = client.get("/maintainance-status/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Estado de mantenimiento no encontrado"
