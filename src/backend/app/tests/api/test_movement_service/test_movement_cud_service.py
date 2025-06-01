from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.testclient import TestClient
from backend.app.api.routes.movement_service.movement_cud_service import router as movement_router
from backend.app.core.conf import headers

app_for_test = FastAPI()
app_for_test.include_router(movement_router)
app_for_test.mount("/static", StaticFiles(directory="src/frontend/static"), name="static")
client = TestClient(app_for_test)

def test_create_movement():
    response = client.post("/movement/create", data={"ID": 1, "IDTipoMovimiento": 2, "Monto": 100, "IDTarjeta":42}, headers=headers)
    assert response.status_code == 201
    data = response.json()
    assert data["success"] is True
    assert data["operation"] == "create"
    assert data["data"]["ID"] == 1

def test_update_movement_existing():
    # Primero lo creamos si no existe
    response = client.post("/movement/update", data={"ID": 1, "IDTipoMovimiento": 2, "Monto": 90000, "IDTarjeta":42}, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["operation"] == "update"
    assert data["data"]["ID"] == 1
    assert data["data"]["Monto"] == 90000

def test_update_movement_not_found():
    response = client.post("/movement/update", data={"ID": 99, "IDTipoMovimiento": 5, "Monto": 2200,"IDTarjeta":42}, headers=headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "Movement not found"

def test_delete_movement_existing():
    # Primero lo creamos si no existe
    response = client.post("/movement/delete", data={"ID":1}, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["operation"] == "delete"
    assert "deleted successfully" in data["message"]

def test_delete_movement_not_found():
    response = client.post("/movement/delete", data={"ID": 999}, headers=headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "Movement not found"

def test_index_create_json():
    response = client.get("/movement/administrador/crear", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "nuevo_id" in data
    assert "typemovements" in data

def test_index_update_json():
    response = client.get("/movement/administrador/actualizar", headers=headers)
    assert response.status_code == 200
    assert "message" in response.json()
    assert "actualización" in response.json()["message"]

def test_index_delete_json():
    response = client.get("/movement/administrador/eliminar", headers=headers)
    assert response.status_code == 200
    assert "message" in response.json()
    assert "eliminación" in response.json()["message"]