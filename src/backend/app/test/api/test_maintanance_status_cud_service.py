from fastapi.testclient import TestClient
from backend.app.api.routes.maintainance_status_CUD_service import app as maintainance_router
from backend.app.logic.universal_controller_sql import UniversalController
from backend.app.models.maintainance_status import MaintainanceStatus

client = TestClient(maintainance_router)

def setup_function():
    """Limpia las tablas antes de cada prueba."""
    UniversalController().clear_tables()

def teardown_function():
    """Limpia las tablas después de cada prueba."""
    UniversalController().clear_tables()

def test_create_status():
    """Prueba la creación de un nuevo estado de mantenimiento."""
    response = client.post(
        "/maintainance-status/create",
        data={"status": "No hecho"}
    )
    assert response.status_code == 303  # Redirección exitosa

def test_create_status_invalid():
    """Prueba la creación de un estado de mantenimiento con un valor inválido."""
    response = client.post(
        "/maintainance-status/create",
        data={"status": "Estado inválido"}
    )
    assert response.status_code == 400  # Error de validación
    assert "El estado 'Estado inválido' no es válido" in response.json()["detail"]

def test_update_status():
    """Prueba la actualización de un estado de mantenimiento existente."""
    # Crear un estado de mantenimiento
    controller = UniversalController()
    created = controller.add(MaintainanceStatus(status="No hecho"))
    status_id = created["id"]

    # Actualizar el estado
    response = client.post(
        "/maintainance-status/update",
        data={"id": status_id, "status": "En progreso"}
    )
    assert response.status_code == 303  # Redirección exitosa

    # Verificar que el estado se actualizó correctamente
    updated = controller.get_by_id(MaintainanceStatus, status_id)
    assert updated.status == "En progreso"

def test_update_status_invalid():
    """Prueba la actualización de un estado de mantenimiento con un valor inválido."""
    # Crear un estado de mantenimiento
    controller = UniversalController()
    created = controller.add(MaintainanceStatus(status="No hecho"))
    status_id = created["id"]

    # Intentar actualizar con un estado inválido
    response = client.post(
        "/maintainance-status/update",
        data={"id": status_id, "status": "Estado inválido"}
    )
    assert response.status_code == 400  # Error de validación
    assert "El estado 'Estado inválido' no es válido" in response.json()["detail"]

def test_delete_status():
    """Prueba la eliminación de un estado de mantenimiento existente."""
    # Crear un estado de mantenimiento
    controller = UniversalController()
    created = controller.add(MaintainanceStatus(status="No hecho"))
    status_id = created["id"]

    # Eliminar el estado
    response = client.post(
        "/maintainance-status/delete",
        data={"id": status_id}
    )
    assert response.status_code == 303  # Redirección exitosa

    # Verificar que el estado fue eliminado
    deleted = controller.get_by_id(MaintainanceStatus, status_id)
    assert deleted is None

def test_delete_status_not_found():
    """Prueba la eliminación de un estado de mantenimiento inexistente."""
    response = client.post(
        "/maintainance-status/delete",
        data={"id": 9999}
    )
    assert response.status_code == 404  # Estado no encontrado
    assert response.json()["detail"] == "Estado de mantenimiento no encontrado"
