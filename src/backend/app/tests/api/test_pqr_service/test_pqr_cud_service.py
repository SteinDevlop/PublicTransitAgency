from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.testclient import TestClient
from backend.app.api.routes.pqr_service.pqr_cud_service import router as pqr_router
from backend.app.core.conf import headers

# App de prueba
app_for_test = FastAPI()
app_for_test.include_router(pqr_router)
app_for_test.mount("/static", StaticFiles(directory="src/frontend/static"), name="static")

client = TestClient(app_for_test)

def test_create_pqr():
    response = client.post(
        "/pqr/create",
        data={
            "ID": 44,
            "identificationuser": 32232,
            "type": "none",
            "description": "aaa",
            "fecha": "29-08-2024"
        },
        headers=headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["success"] is True
    assert data["operation"] == "create"
    assert data["data"]["ID"] == 44
    assert data["data"]["type"] == "none"
    assert data["data"]["description"] == "aaa"
    assert data["data"]["fecha"] == "29-08-2024"
    assert data["data"]["identificationuser"] == 32232

def test_update_pqr_existing():
    # Asegurar existencia antes de actualizar
    response = client.post(
        "/pqr/update",
        data={
            "ID": 44,
            "identificationuser":32232,
            "type": "tipo2",
            "description": "desc2",
            "fecha": "01-01-2025"
        },
        headers=headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["operation"] == "update"
    assert data["data"]["ID"] == 44
    assert data["data"]["type"] == "tipo2"
    assert data["data"]["description"] == "desc2"
    assert data["data"]["fecha"] == "01-01-2025"
    assert data["data"]["identificationuser"] == 32232

def test_update_pqr_not_found():
    response = client.post(
        "/pqr/update",
        data={
            "ID": 999,
            "identificationuser": 77,
            "type": "bb",
            "description": "aaa",
            "fecha": "29-08-2024"
        },
        headers=headers,
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "PQR not found"

def test_delete_pqr_existing():
    # Asegurar existencia antes de borrar
    response = client.post(
        "/pqr/delete",
        data={"ID": 44},
        headers=headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["operation"] == "delete"
    assert "deleted" in data["message"]

def test_delete_pqr_not_found():
    response = client.post(
        "/pqr/delete",
        data={"ID": 999},
        headers=headers,
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "PQR not found"

def test_index_create_form():
    response = client.get("/pqr/administrador/crear", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "nuevo_id" in data
    assert "message" in data

def test_index_update_form():
    response = client.get("/pqr/administrador/actualizar", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "actualización" in data["message"]

def test_index_delete_form():
    response = client.get("/pqr/administrador/eliminar", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "eliminación" in data["message"]