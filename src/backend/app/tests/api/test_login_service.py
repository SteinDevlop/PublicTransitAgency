import pytest
from fastapi.testclient import TestClient
from backend.app.api.routes.login_service import app as login_router
from backend.app.logic.universal_controller_instance import universal_controller as controller
from backend.app.models.user import UserOut,UserCreate
from fastapi import FastAPI

app_for_test = FastAPI()
app_for_test.include_router(login_router)
client = TestClient(app_for_test)

@pytest.fixture
def test_user():
    # Crea un usuario de prueba con todos los campos requeridos
    user = UserCreate(
        ID=9999,
        Identificacion=123456,
        Nombre="TestUser",
        Apellido="TestApellido",
        Correo="testuser@example.com",
        Contrasena="testpass",
        IDRolUsuario=1,
        IDTurno=1,
        IDTarjeta=1
    )
    existing = controller.get_by_id(UserCreate, user.ID)
    if existing:
        controller.delete(existing)
    controller.add(user)
    yield user
    controller.delete(user)

def test_login_success(test_user):
    response = client.post("/login/token", data={"username": str(test_user.ID), "password": "testpass"})
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_fail_wrong_password(test_user):
    response = client.post("/login/token", data={"username": str(test_user.ID), "password": "wrongpass"})
    assert response.status_code == 401

def test_login_fail_wrong_user():
    response = client.post("/login/token", data={"username": "999999", "password": "testpass"})
    assert response.status_code == 401

def test_dashboard_no_auth():
    response = client.get("/login/dashboard")
    assert response.status_code == 401
    login = client.post("/login/token", data={"username": str(test_user.ID), "password": "testpass"})
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/login/dashboard", headers=headers)
    assert response.status_code == 200
    assert "user" in response.json()

def test_dashboard_no_auth():
    response = client.get("/login/dashboard")
    assert response.status_code == 401
