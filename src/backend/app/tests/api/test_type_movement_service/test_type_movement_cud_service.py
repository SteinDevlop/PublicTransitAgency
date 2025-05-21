from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.testclient import TestClient
from backend.app.api.routes.type_movement_service.type_movement_cud_service import router as typemovement_router
from backend.app.core.conf import headers

# Creamos la app de prueba
app_for_test = FastAPI()
app_for_test.include_router(typemovement_router)
app_for_test.mount("/static", StaticFiles(directory="src/frontend/static"), name="static")

client = TestClient(app_for_test)

def test_create_typemovement():
    response = client.post(
        "/typemovement/create",
        data={"ID": 1, "TipoMovimiento": "ingreso_sistema"},
        headers=headers
    )
    assert response.status_code == 201
    data = response.json()
    assert data["success"] is True
    assert data["operation"] == "create"
    assert data["data"]["ID"] == 1
    assert data["data"]["TipoMovimiento"] == "ingreso_sistema"

def test_update_typemovement_existing():
    # Creamos primero si no existe
    client.post(
        "/typemovement/create",
        data={"ID": 2, "TipoMovimiento": "egreso_sistema"},
        headers=headers
    )
    response = client.post(
        "/typemovement/update",
        data={"ID": 2, "TipoMovimiento": "recarga"},
        headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["operation"] == "update"
    assert data["data"]["ID"] == 2
    assert data["data"]["TipoMovimiento"] == "recarga"

def test_update_typemovement_not_found():
    response = client.post(
        "/typemovement/update",
        data={"ID": 99, "TipoMovimiento": "ninguno"},
        headers=headers
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "TypeMovement not found"

def test_delete_typemovement_existing():
    # Creamos primero si no existe
    client.post(
        "/typemovement/create",
        data={"ID": 3, "TipoMovimiento": "borrado"},
        headers=headers
    )
    response = client.post(
        "/typemovement/delete",
        data={"ID": 3},
        headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["operation"] == "delete"
    assert "deleted" in data["message"]

def test_delete_typemovement_not_found():
    response = client.post(
        "/typemovement/delete",
        data={"ID": 999},
        headers=headers
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "TypeMovement not found"

def test_index_create_form():
    response = client.get("/typemovement/crear", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "creación" in data["message"]

def test_index_update_form():
    response = client.get("/typemovement/actualizar", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "actualización" in data["message"]

def test_index_delete_form():
    response = client.get("/typemovement/eliminar", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "eliminación" in data["message"]