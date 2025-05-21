from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.testclient import TestClient
from backend.app.api.routes.behavior_service.behavior_cud_service import router as behavior_router
from backend.app.core.conf import headers

app_for_test = FastAPI()
app_for_test.include_router(behavior_router)
app_for_test.mount("/static", StaticFiles(directory="src/frontend/static"), name="static")
client = TestClient(app_for_test)

def test_create_behavior():
    response = client.post(
        "/behavior/create",
        data={
            "ID": 44,
            "iduser": 33,
            "cantidadrutas": 2,
            "horastrabajadas": 12,
            "observaciones": "none",
            "fecha": "29-08-2024"
        },
        headers=headers
    )
    assert response.status_code == 201
    data = response.json()
    assert data["data"]["ID"] == 44
    assert data["data"]["observaciones"] == "none"
    assert data["success"] is True
    assert data["operation"] == "create"

def test_update_behavior_existing():
    # Asegura que existe primero
    response = client.post(
        "/behavior/update",
        data={
            "ID": 44,
            "iduser": 33,
            "cantidadrutas": 3,
            "horastrabajadas": 12,
            "observaciones": "milei",
            "fecha": "29-08-2024"
        },
        headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["observaciones"] == "milei"
    assert data["data"]["cantidadrutas"] == 3
    assert data["success"] is True
    assert data["operation"] == "update"

def test_update_behavior_not_found():
    response = client.post(
        "/behavior/update",
        data={
            "ID": 999,
            "iduser": 99,
            "cantidadrutas": 3,
            "horastrabajadas": 12,
            "observaciones": "milei",
            "fecha": "29-08-2024"
        },
        headers=headers
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Behavior not found"

def test_delete_behavior_existing():
    # Asegura que existe primero
    response = client.post(
        "/behavior/delete",
        data={"ID": 44},
        headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    assert "deleted" in data["message"]
    assert data["success"] is True
    assert data["operation"] == "delete"

def test_delete_behavior_not_found():
    response = client.post(
        "/behavior/delete",
        data={"ID": 999},
        headers=headers
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Behavior not found"

def test_index_create_supervisor():
    response = client.get("/behavior/supervisor/crear", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "nuevo_id" in data
    assert "behaviors" in data

def test_index_create_admin():
    response = client.get("/behavior/administrador/crear", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "nuevo_id" in data
    assert "behaviors" in data

def test_index_update_form():
    response = client.get("/behavior/administrador/actualizar", headers=headers)
    assert response.status_code == 200
    assert "message" in response.json()
    assert "actualización" in response.json()["message"]

def test_index_delete_form():
    response = client.get("/behavior/administrador/eliminar", headers=headers)
    assert response.status_code == 200
    assert "message" in response.json()
    assert "eliminación" in response.json()["message"]