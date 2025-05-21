from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.testclient import TestClient
from backend.app.api.routes.type_transport_service.type_transport_cud_service import router as typetransport_router
from backend.app.core.conf import headers

# Creamos la app de prueba
app_for_test = FastAPI()
app_for_test.include_router(typetransport_router)
app_for_test.mount("/static", StaticFiles(directory="src/frontend/static"), name="static")

# Cliente de prueba
client = TestClient(app_for_test)

def test_create_transport():
    response = client.post(
        "/typetransport/create",
        data={"ID": 1, "TipoTransporte": "aaaaa"},
        headers=headers
    )
    assert response.status_code == 201
    data = response.json()
    assert data["success"] is True
    assert data["operation"] == "create"
    assert data["data"]["ID"] == 1
    assert data["data"]["TipoTransporte"] == "aaaaa"

def test_update_transport_existing():
    # Creamos primero un transporte para asegurar que existe
    client.post(
        "/typetransport/create",
        data={"ID": 2, "TipoTransporte": "bus"},
        headers=headers
    )
    # Luego actualizarlo
    response = client.post(
        "/typetransport/update",
        data={"ID": 2, "TipoTransporte": "railway"},
        headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["operation"] == "update"
    assert data["data"]["ID"] == 2
    assert data["data"]["TipoTransporte"] == "railway"

def test_update_transport_not_found():
    response = client.post(
        "/typetransport/update",
        data={"ID": 99, "TipoTransporte": "ninguno"},
        headers=headers
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "TypeTransport not found"

def test_delete_transport_existing():
    # Creamos primero el transporte si no existe
    client.post(
        "/typetransport/create",
        data={"ID": 3, "TipoTransporte": "metro"},
        headers=headers
    )
    response = client.post(
        "/typetransport/delete",
        data={"ID": 3},
        headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["operation"] == "delete"
    assert "deleted" in data["message"]

def test_delete_transport_not_found():
    response = client.post(
        "/typetransport/delete",
        data={"ID": 999},
        headers=headers
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "TypeTransport not found"

def test_index_create_form():
    response = client.get("/typetransport/crear", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "creación" in data["message"]

def test_index_update_form():
    response = client.get("/typetransport/actualizar", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "actualización" in data["message"]

def test_index_delete_form():
    response = client.get("/typetransport/eliminar", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "eliminación" in data["message"]