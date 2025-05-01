from fastapi.testclient import TestClient
from backend.app.api.routes.incidence_cud_service import app as incidences_router
from backend.app.logic.universal_controller_sql import UniversalController
from backend.app.models.incidence import Incidence

client = TestClient(incidences_router)

def setup_function():
    """Limpia las tablas antes de cada prueba."""
    UniversalController().clear_tables()

def test_crear_incidencia():
    """Prueba la creación de una nueva incidencia."""
    response = client.post("/incidence/create", data={"description": "Accidente", "status": "Abierto", "type": "Choque"})
    assert response.status_code == 303  # Redirección exitosa

def test_actualizar_incidencia():
    """Prueba la actualización de una incidencia existente."""
    controller = UniversalController()
    controller.add(Incidence(incidence_id=1, description="Accidente", status="Abierto", type="Choque"))
    response = client.post("/incidence/update", data={"incidence_id": 1, "description": "Actualizado", "status": "Cerrado", "type": "Nuevo tipo"})
    assert response.status_code == 303  # Redirección exitosa

def test_actualizar_incidencia_no_existente():
    """Prueba la actualización de una incidencia inexistente."""
    response = client.post("/incidence/update", data={"incidence_id": 999, "description": "Fallido", "status": "Abierto", "type": "Choque"})
    assert response.status_code == 404  # Incidencia no encontrada

def test_eliminar_incidencia():
    """Prueba la eliminación de una incidencia existente."""
    controller = UniversalController()
    controller.add(Incidence(incidence_id=1, description="Accidente", status="Abierto", type="Choque"))
    response = client.post("/incidence/delete", data={"incidence_id": 1})
    assert response.status_code == 303  # Redirección exitosa

def test_eliminar_incidencia_no_existente():
    """Prueba la eliminación de una incidencia inexistente."""
    response = client.post("/incidence/delete", data={"incidence_id": 999})
    assert response.status_code == 404  # Incidencia no encontrada