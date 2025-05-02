from fastapi import FastAPI
from fastapi.testclient import TestClient
from backend.app.api.routes.maintainance_status_CUD_service import app as status_router
from backend.app.models.maintainance_status import MaintainanceStatus

app_for_test = FastAPI()
app_for_test.include_router(status_router)
client = TestClient(app_for_test)

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
    # Crear un estado de mantenimiento para actualizar
    create_response = client.post(
        "/maintainance-status/create",
        data={"status": "No hecho"}
    )
    assert create_response.status_code == 303

    # Obtener el ID del estado creado
    response = client.get("/maintainance-status/")
    assert response.status_code == 200
    data = response.json()
    status_id = data[0]["id"]

    # Actualizar el estado
    update_response = client.post(
        "/maintainance-status/update",
        data={"id": status_id, "status": "En progreso"}
    )
    assert update_response.status_code == 303  # Redirección exitosa

    # Verificar que el estado se actualizó correctamente
    response = client.get(f"/maintainance-status/{status_id}")
    assert response.status_code == 200
    updated_data = response.json()
    assert updated_data["status"] == "En progreso"

def test_update_status_invalid():
    """Prueba la actualización de un estado de mantenimiento con un valor inválido."""
    # Crear un estado de mantenimiento para actualizar
    create_response = client.post(
        "/maintainance-status/create",
        data={"status": "No hecho"}
    )
    assert create_response.status_code == 303

    # Obtener el ID del estado creado
    response = client.get("/maintainance-status/")
    assert response.status_code == 200
    data = response.json()
    status_id = data[0]["id"]

    # Intentar actualizar con un estado inválido
    update_response = client.post(
        "/maintainance-status/update",
        data={"id": status_id, "status": "Estado inválido"}
    )
    assert update_response.status_code == 400  # Error de validación
    assert "El estado 'Estado inválido' no es válido" in update_response.json()["detail"]

def test_delete_status():
    """Prueba la eliminación de un estado de mantenimiento existente."""
    # Crear un estado de mantenimiento para eliminar
    create_response = client.post(
        "/maintainance-status/create",
        data={"status": "No hecho"}
    )
    assert create_response.status_code == 303

    # Obtener el ID del estado creado
    response = client.get("/maintainance-status/")
    assert response.status_code == 200
    data = response.json()
    status_id = data[0]["id"]

    # Eliminar el estado
    delete_response = client.post(
        "/maintainance-status/delete",
        data={"id": status_id}
    )
    assert delete_response.status_code == 303  # Redirección exitosa

    # Verificar que el estado fue eliminado
    response = client.get(f"/maintainance-status/{status_id}")
    assert response.status_code == 404  # Estado no encontrado

def test_delete_status_not_found():
    """Prueba la eliminación de un estado de mantenimiento inexistente."""
    response = client.post(
        "/maintainance-status/delete",
        data={"id": 9999}
    )
    assert response.status_code == 404  # Estado no encontrado
    assert response.json()["detail"] == "Maintainance status not found"
