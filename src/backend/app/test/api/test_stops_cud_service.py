import pytest
from fastapi.testclient import TestClient
from backend.app.api.routes.stops_CUD_service import stop_router
from backend.app.logic.universal_controller_sql import UniversalController
from backend.app.models.stops import StopCreate

# Cliente de prueba
client = TestClient(stop_router)

def setup_function():
    """Limpia las tablas antes de cada prueba."""
    UniversalController().clear_tables()

def test_crear_parada():
    """Prueba la creación de una nueva parada."""
    response = client.post("/stop/create", data={"stop_id": 1, "name": "Parada 1", "location": "Ubicación 1"})
    assert response.status_code == 303  # Redirección exitosa

def test_actualizar_parada_existente():
    """Prueba la actualización de una parada existente."""
    controller = UniversalController()
    controller.add(StopCreate(stop_id=1, stop_data={"name": "Parada 1", "location": "Ubicación 1"}))
    response = client.post("/stop/update", data={"stop_id": 1, "name": "Parada Actualizada", "location": "Nueva Ubicación"})
    assert response.status_code == 303  # Redirección exitosa

def test_actualizar_parada_no_existente():
    """Prueba la actualización de una parada que no existe."""
    response = client.post("/stop/update", data={"stop_id": 999, "name": "Parada Inexistente", "location": "Ubicación"})
    assert response.status_code == 404  # Parada no encontrada

def test_eliminar_parada_existente():
    """Prueba la eliminación de una parada existente."""
    controller = UniversalController()
    controller.add(StopCreate(stop_id=1, stop_data={"name": "Parada 1", "location": "Ubicación 1"}))
    response = client.post("/stop/delete", data={"stop_id": 1})
    assert response.status_code == 303  # Redirección exitosa

def test_eliminar_parada_no_existente():
    """Prueba la eliminación de una parada que no existe."""
    response = client.post("/stop/delete", data={"stop_id": 999})
    assert response.status_code == 404  # Parada no encontrada