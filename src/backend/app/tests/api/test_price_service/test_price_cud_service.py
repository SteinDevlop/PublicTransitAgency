from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.testclient import TestClient
from backend.app.api.routes.price_service.price_cud_service import router as price_router
from backend.app.core.conf import headers

app_for_test = FastAPI()
app_for_test.include_router(price_router)
app_for_test.mount("/static", StaticFiles(directory="src/frontend/static"), name="static")

client = TestClient(app_for_test)

def test_create_price():
    response = client.post(
        "/price/create",
        data={"ID": 3, "IDTipoTransporte": 2, "Monto": 100},
        headers=headers
    )
    # Nuevo servicio: respuesta debe ser 201 y JSON
    assert response.status_code == 201
    data = response.json()
    assert data["success"] is True
    assert data["operation"] == "create"
    assert data["data"]["ID"] == 3
    assert data["data"]["IDTipoTransporte"] == 2
    assert data["data"]["Monto"] == 100

def test_update_price_existing():
    response = client.post(
        "/price/update",
        data={"ID": 3, "IDTipoTransporte": 2, "Monto": 250},
        headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["operation"] == "update"
    assert data["data"]["ID"] == 3
    assert data["data"]["IDTipoTransporte"] == 2
    assert data["data"]["Monto"] == 250

def test_update_price_not_found():
    response = client.post(
        "/price/update",
        data={"ID": 99, "IDTipoTransporte": 5, "Monto": 2200},
        headers=headers
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Price not found"

def test_delete_price_existing():
    response = client.post(
        "/price/delete",
        data={"ID": 3},
        headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["operation"] == "delete"
    assert "deleted" in data["message"]

def test_delete_price_not_found():
    response = client.post(
        "/price/delete",
        data={"ID": 999},
        headers=headers
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Price not found"

def test_index_create_form():
    response = client.get("/price/administrador/crear", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "creación" in data["message"]
    assert "nuevo_id" in data

def test_index_update_form():
    response = client.get("/price/administrador/actualizar", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "actualización" in data["message"]

def test_index_delete_form():
    response = client.get("/price/administrador/eliminar", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "eliminación" in data["message"]