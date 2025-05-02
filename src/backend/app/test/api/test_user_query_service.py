import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from backend.app.api.routes.user_query_service import app as user_router
from backend.app.logic.universal_controller_sql import UniversalController
from backend.app.models.user import UserOut


def setup_function():
    UniversalController().clear_tables()

def teardown_function():
    UniversalController().clear_tables()

# Mock para UniversalController
class MockUniversalController:
    def __init__(self):
        # Datos simulados de tipos de tarjeta
        self.users = {
            3: UserOut(
                    id=3,
                    identification=12345678,
                    name="John",
                    lastname="Doe",
                    email="johndoe@example.com",
                    password="password@123",
                    idtype_user=1,
                    idturn=1,
                ),
        }

    def read_all(self, model):
        """Simula obtener todos los usuarios"""
        return list(self.users.values())

    def get_by_id(self, model, id_: int):
        """Simula obtener un usuario por ID"""
        return self.users.get(id_)

# Patching el controller en tests
@pytest.fixture(autouse=True)
def override_controller(monkeypatch):
    """Fixture para reemplazar el controlador real por el mock"""
    from backend.app.api.routes.user_query_service import controller
    monkeypatch.setattr(controller, "read_all", MockUniversalController().read_all)
    monkeypatch.setattr(controller, "get_by_id", MockUniversalController().get_by_id)

test_app = FastAPI()
test_app.include_router(user_router)
client = TestClient(test_app)

# Test GET /consultar (vista HTML)

def test_read_all():
    """Prueba que la ruta '/user/' devuelve todos los tipos de transporte."""
    response = client.get("/user/users/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == 3
    assert data[0]["identification"] == 12345678
    assert data[0]["name"] == "John"
    assert data[0]["lastname"] == "Doe"
    assert data[0]["email"] == "johndoe@example.com"
    assert data[0]["password"] == "password@123"
    assert data[0]["idtype_user"] == 1
    assert data[0]["idturn"] == 1

def test_get_by_id():
    """Prueba que la ruta '/typetransport/{id}' devuelve el tipo de transporte correcto."""
    response = client.get("/user/3")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 3
    assert data["identification"] == 12345678
    assert data["name"] == "John"
    assert data["lastname"] == "Doe"
    assert data["email"] == "johndoe@example.com"
    assert data["password"] == "password@123"
    assert data["idtype_user"] == 1
    assert data["idturn"] == 1

def test_get_by_id_not_found():
    """Prueba que la ruta '/typetransport/{id}' devuelve un error 404 si no se encuentra el tipo de transporte."""
    response = client.get("/typetransport/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}

