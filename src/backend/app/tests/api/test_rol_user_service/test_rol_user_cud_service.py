from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.testclient import TestClient
from backend.app.api.routes.rol_user_service.rol_user_cud_service import router as roluser_router
from backend.app.core.conf import headers

# Creamos la app de prueba
app_for_test = FastAPI()
app_for_test.include_router(roluser_router)
app_for_test.mount("/static", StaticFiles(directory="src/frontend/static"), name="static")

client = TestClient(app_for_test)

def test_create_roluser():
    response = client.post("/roluser/create", data={"ID": 6, "Rol": "aaa"}, headers=headers)
    assert response.status_code == 201
    data = response.json()
    assert data["success"] is True
    assert data["operation"] == "create"
    assert data["data"]["ID"] == 6
    assert data["data"]["Rol"] == "aaa"

def test_update_roluser_existing():
    # Creamos primero el roluser si no existe
    client.post("/roluser/create", data={"ID": 7, "Rol": "bbb"}, headers=headers)
    response = client.post("/roluser/update", data={"ID": 7, "Rol": "nnn"}, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["operation"] == "update"
    assert data["data"]["ID"] == 7
    assert data["data"]["Rol"] == "nnn"

def test_update_roluser_not_found():
    response = client.post("/roluser/update", data={"ID": 99, "Rol": "administrador"}, headers=headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "RolUser not found"

def test_delete_roluser_existing():
    # Creamos primero el roluser si no existe
    client.post("/roluser/create", data={"ID": 8, "Rol": "ccc"}, headers=headers)
    response = client.post("/roluser/delete", data={"ID": 8}, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["operation"] == "delete"
    assert "deleted" in data["message"]

def test_delete_roluser_not_found():
    response = client.post("/roluser/delete", data={"ID": 999}, headers=headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "RolUser not found"

def test_index_create_form():
    response = client.get("/roluser/crear", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "creación" in data["message"]
    assert "nuevo_id" in data

def test_index_update_form():
    response = client.get("/roluser/actualizar", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "actualización" in data["message"]

def test_index_delete_form():
    response = client.get("/roluser/eliminar", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "eliminación" in data["message"]