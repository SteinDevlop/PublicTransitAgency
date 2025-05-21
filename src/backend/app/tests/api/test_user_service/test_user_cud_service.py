from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.testclient import TestClient
from backend.app.api.routes.user_service.user_CUD_service import router as user_router
from backend.app.core.conf import headers

# App de prueba
app_for_test = FastAPI()
app_for_test.include_router(user_router)
app_for_test.mount("/static", StaticFiles(directory="src/frontend/static"), name="static")

client = TestClient(app_for_test)

def test_create_user():
    response = client.post(
        "/user/create",
        data={
            "ID": 1,
            "Identificacion": 99,
            "Nombre": "aa",
            "Apellido": "bb",
            "Correo": "prueba12121@gmail.com",
            "Contrasena": "1234@1234Aasss",
            "IDRolUsuario": 1,
            "IDTurno": 1,
            "IDTarjeta": 1
        },
        headers=headers
    )
    assert response.status_code == 201
    data = response.json()
    assert data["success"] is True
    assert data["operation"] == "create"
    assert data["data"]["ID"] == 1
    assert data["data"]["Nombre"] == "aa"

def test_update_user_existing():
    # Asegurarse de que el usuario existe primero
    client.post(
        "/user/create",
        data={
            "ID": 2,
            "Identificacion": 123,
            "Nombre": "cc",
            "Apellido": "dd",
            "Correo": "correoexistente@example.com",
            "Contrasena": "1234@1234Aasss",
            "IDRolUsuario": 1,
            "IDTurno": 1,
            "IDTarjeta": 1
        },
        headers=headers
    )
    response = client.post(
        "/user/update",
        data={
            "ID": 2,
            "Identificacion": 124,
            "Nombre": "ee",
            "Apellido": "ff",
            "Correo": "correoactualizado@example.com",
            "Contrasena": "1234@1234Aasss",
            "IDRolUsuario": 2,
            "IDTurno": 1,
            "IDTarjeta": 2
        },
        headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["operation"] == "update"
    assert data["data"]["Nombre"] == "ee"
    assert data["data"]["Correo"] == "correoactualizado@example.com"

def test_update_user_not_found():
    response = client.post(
        "/user/update",
        data={
            "ID": 999,
            "Identificacion": 99,
            "Nombre": "aa",
            "Apellido": "bb",
            "Correo": "prueba@gmail.com",
            "Contrasena": "1234@1234Aasss",
            "IDRolUsuario": 1,
            "IDTurno": 1,
            "IDTarjeta": 1
        },
        headers=headers
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"

def test_delete_user_existing():
    # Crear primero el usuario para poder eliminarlo
    client.post(
        "/user/create",
        data={
            "ID": 3,
            "Identificacion": 333,
            "Nombre": "gg",
            "Apellido": "hh",
            "Correo": "paraborrar@example.com",
            "Contrasena": "1234@1234Aasss",
            "IDRolUsuario": 1,
            "IDTurno": 1,
            "IDTarjeta": 1
        },
        headers=headers
    )
    response = client.post(
        "/user/delete",
        data={"ID": 3},
        headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["operation"] == "delete"
    assert "deleted" in data["message"]

def test_delete_user_not_found():
    response = client.post(
        "/user/delete",
        data={"ID": 999},
        headers=headers
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"

def test_index_create_form():
    response = client.get("/user/crear", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "nuevo_id" in data
    assert "roles" in data
    assert "turnos" in data

def test_index_update_form():
    response = client.get("/user/actualizar", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "actualización" in data["message"]

def test_index_delete_form():
    response = client.get("/user/eliminar", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "eliminación" in data["message"]