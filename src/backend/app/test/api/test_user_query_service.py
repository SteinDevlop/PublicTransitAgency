# tests/test_user_consult_routes.py

"""import pytest
from fastapi.testclient import TestClient
from src.backend.app.api.routes.user import app  # importa tu router correcto
from fastapi import FastAPI

# Montar una app para test
test_app = FastAPI()
test_app.include_router(app)
client = TestClient(test_app)

# Mock para UniversalController
class MockController:
    def read_all(self, model):
        return [
            {
                "id": 1,
                "identification": 12345678,
                "name": "John",
                "lastname": "Doe",
                "email": "john@example.com",
                "password": "secret",
                "idtype_user": 1,
                "idturn": 2
            },
            {
                "id": 2,
                "identification": 87654321,
                "name": "Jane",
                "lastname": "Smith",
                "email": "jane@example.com",
                "password": "hidden",
                "idtype_user": 2,
                "idturn": 3
            }
        ]

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
                "idturn": 2
            }
        else:
            return None

# Patching el controller en tests
@pytest.fixture(autouse=True)
def override_controller(monkeypatch):
    from src.backend.app.api.routes import user
    user.controller = MockController()

# Test GET /consultar (vista HTML)

def test_consultar_usuario_get():
    response = client.get("/user/consultar")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]

# Test GET /usuarios (listar todos los usuarios)

def test_get_usuarios():
    response = client.get("/user/usuarios")
    assert response.status_code == 200
    json_data = response.json()
    assert isinstance(json_data, list)
    assert len(json_data) == 2
    assert json_data[0]["name"] == "John"
    assert json_data[1]["name"] == "Jane"

# Test GET /usuario?id=1 (usuario existente)

def test_get_usuario_existente():
    response = client.get("/user/usuario?id=1")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "John" in response.text  # Validamos que el HTML tenga el nombre del usuario

# Test GET /usuario?id=999 (usuario no existente)

def test_get_usuario_no_existente():
    response = client.get("/user/usuario?id=999")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "none" in response.text  # El template muestra 'none' si no encuentra el usuario"""
