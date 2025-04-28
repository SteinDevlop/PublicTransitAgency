# tests/test_user_routes.py

"""import pytest
from fastapi.testclient import TestClient
from src.backend.app.api.routes.user import app  # importa tu router correcto
from fastapi import FastAPI

# Montar una app para test
test_app = FastAPI()
test_app.include_router(app)
client = TestClient(test_app)

# Test GET routes (crear, eliminar, actualizar)

def test_crear_usuario_get():
    response = client.get("/user/crear")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]

def test_eliminar_usuario_get():
    response = client.get("/user/eliminar")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]

def test_actualizar_usuario_get():
    response = client.get("/user/actualizar")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]

# Mock para UniversalController
class MockController:
    def add(self, data):
        return True

    def get_by_id(self, model, id):
        if id == 1:
            return {
                "id": 1,
                "identification": 12345678,
                "name": "John",
                "lastname": "Doe",
                "email": "john@example.com",
                "password": "secret",
                "idtype_user": 1,
                "idturn": 1
            }
        else:
            return None

    def update(self, data):
        return True

    def delete(self, data):
        return True

# Patching el controller en tests
@pytest.fixture(autouse=True)
def override_controller(monkeypatch):
    from src.backend.app.api.routes import user
    user.controller = MockController()

# Test POST /create

def test_create_user_post():
    response = client.post("/user/create", data={
        "id": 1,
        "identification": 12345678,
        "name": "John",
        "lastname": "Doe",
        "email": "john@example.com",
        "password": "secret",
        "idtype_user": 1,
        "idturn": 2
    })
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["operation"] == "create"
    assert json_data["success"] is True
    assert json_data["data"]["name"] == "John"

# Test POST /update para usuario existente

def test_update_user_post_success():
    response = client.post("/user/update", data={
        "id": 1,
        "identification": 87654321,
        "name": "Johnny",
        "lastname": "DoeUpdated",
        "email": "johnny@example.com",
        "password": "newsecret",
        "idtype_user": 2,
        "idturn": 3
    })
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["operation"] == "update"
    assert json_data["success"] is True
    assert json_data["data"]["name"] == "Johnny"

# Test POST /update para usuario no encontrado

def test_update_user_post_not_found():
    response = client.post("/user/update", data={
        "id": 999,  # id no existente
        "identification": 87654321,
        "name": "Ghost",
        "lastname": "User",
        "email": "ghost@example.com",
        "password": "nooneknows",
        "idtype_user": 2,
        "idturn": 3
    })
    assert response.status_code == 404
    assert response.json() == {"detail": "Usuario no encontrada"}

# Test POST /delete para usuario existente

def test_delete_user_post_success():
    response = client.post("/user/delete", data={
        "id": 1,
    })
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["operation"] == "delete"
    assert json_data["success"] is True

# Test POST /delete para usuario no encontrado

def test_delete_user_post_not_found():
    response = client.post("/user/delete", data={
        "id": 999,  # id no existente
    })
    assert response.status_code == 404
    assert response.json() == {"detail": "Usuario no encontrado"}"""
