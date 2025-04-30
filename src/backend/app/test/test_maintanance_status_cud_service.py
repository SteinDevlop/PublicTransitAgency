"""from fastapi import FastAPI
from fastapi.testclient import TestClient
from backend.app.api.main import app as maintainance_app # Asegúrate de la ruta correcta a tu app

# Crear la aplicación de prueba
app_for_test = FastAPI()
app_for_test.mount("/", maintainance_app) # Monta la aplicación principal

# Cliente de prueba
client = TestClient(app_for_test)

def test_show_create_form():
    response = client.get("/maintainance_status/crear")
    assert response.status_code == 200
    assert "Crear Estado de Mantenimiento" in response.text # Verifica contenido específico del formulario

def test_show_update_form():
    response = client.get("/maintainance_status/actualizar")
    assert response.status_code == 200
    assert "Actualizar Estado de Mantenimiento" in response.text # Verifica contenido específico del formulario

def test_show_delete_form():
    response = client.get("/maintainance_status/eliminar")
    assert response.status_code == 200
    assert "Eliminar Estado de Mantenimiento" in response.text # Verifica contenido específico del formulario

def test_create_status():
    response = client.post(
        "/maintainance_status/create",
        data={"id": 5, "unit": "Unidad F", "type": "Urgente", "status": "pendiente"}
    )
    assert response.status_code == 200
    assert response.json()["id"] == 5
    assert response.json()["unit"] == "Unidad F"
    assert response.json()["type"] == "Urgente"
    assert response.json()["status"] == "pendiente"

def test_create_status_validation_error():
    response = client.post(
        "/maintainance_status/create",
        data={"id": 6, "unit": "Unidad G", "type": "Anual", "status": "invalido"}
    )
    assert response.status_code == 400
    assert "Estado debe ser uno de" in response.json()["detail"]

def test_update_status_existing():
    # Primero crea un estado para actualizarlo
    client.post(
        "/maintainance_status/create",
        data={"id": 7, "unit": "Unidad H", "type": "Semanal", "status": "activo"}
    )
    response = client.post(
        "/maintainance_status/update",
        data={"id": 7, "unit": "Unidad H Updated", "type": "Semanal", "status": "completado"}
    )
    assert response.status_code == 200
    assert response.json()["id"] == 7
    assert response.json()["unit"] == "Unidad H Updated"
    assert response.json()["status"] == "completado"

def test_update_status_not_found():
    response = client.post(
        "/maintainance_status/update",
        data={"id": 999, "unit": "Unidad I", "type": "Mensual", "status": "activo"}
    )
    assert response.status_code == 404
    assert "Registro no encontrado" in response.json()["detail"]

def test_delete_status_existing():
    # Primero crea un estado para eliminarlo
    client.post(
        "/maintainance_status/create",
        data={"id": 8, "unit": "Unidad J", "type": "Diario", "status": "en_proceso"}
    )
    response = client.post(
        "/maintainance_status/delete",
        data={"id": 8}
    )
    assert response.status_code == 200
    assert "Estado 8 eliminado correctamente" in response.json()["message"]

def test_delete_status_not_found():
    response = client.post(
        "/maintainance_status/delete",
        data={"id": 999}
    )
    assert response.status_code == 404
    assert "Registro no encontrado" in response.json()["detail"]"""