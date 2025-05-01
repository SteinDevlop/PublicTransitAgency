<<<<<<< HEAD
"""import pytest
=======
import pytest
>>>>>>> 84f3392 (updating tests)
from fastapi.testclient import TestClient
from backend.app.models.rol_user import RolUserOut
from fastapi import FastAPI
from backend.app.api.routes.rol_user_query_service import app as roluser_router
from backend.app.logic.universal_controller_sql import UniversalController
def setup_function():
    UniversalController().clear_tables()

def teardown_function():
    UniversalController().clear_tables()
# Mock de la clase UniversalController
class MockUniversalController:
    def __init__(self):
        # Datos simulados de tipos de usuario
        self.rolusers = {
            3: RolUserOut(id=3, type="admin"),  # Tipo de usuario con id=3
            4: RolUserOut(id=4, type="driver"),  # Tipo de usuario con id=4
        }

    def read_all(self, model):
<<<<<<< HEAD
        ///Simula obtener todos los tipos de usuario///
        return list(self.rolusers.values())

    def get_by_id(self, model, id_: int):
        ///Simula obtener un tipo de usuario por ID///
=======
        """Simula obtener todos los tipos de usuario"""
        return list(self.rolusers.values())

    def get_by_id(self, model, id_: int):
        """Simula obtener un tipo de usuario por ID"""
>>>>>>> 84f3392 (updating tests)
        return self.rolusers.get(id_)

@pytest.fixture(autouse=True)
def override_controller(monkeypatch):
<<<<<<< HEAD
    ///Fixture para reemplazar el controlador real por el mock///
=======
    """Fixture para reemplazar el controlador real por el mock"""
>>>>>>> 84f3392 (updating tests)
    from backend.app.api.routes.rol_user_query_service import controller
    monkeypatch.setattr(controller, "read_all", MockUniversalController().read_all)
    monkeypatch.setattr(controller, "get_by_id", MockUniversalController().get_by_id)

# Crear la aplicación de prueba
app_for_test = FastAPI()
app_for_test.include_router(roluser_router)

client = TestClient(app_for_test)

def test_read_all():
<<<<<<< HEAD
    ///Prueba que la ruta '/rolusers/' devuelve todos los tipos de usuario.///
=======
    """Prueba que la ruta '/rolusers/' devuelve todos los tipos de usuario."""
>>>>>>> 84f3392 (updating tests)
    response = client.get("/roluser/rolusers/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["id"] == 3
    assert data[0]["type"] == "admin"
    assert data[1]["id"] == 4
    assert data[1]["type"] == "driver"

def test_get_by_id():
<<<<<<< HEAD
    ///Prueba que la ruta '/roluser/{id}' devuelve el tipo de usuario correcto.///
=======
    """Prueba que la ruta '/roluser/{id}' devuelve el tipo de usuario correcto."""
>>>>>>> 84f3392 (updating tests)
    response = client.get("/roluser/4")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 4
    assert data["type"] == "driver"

def test_get_by_id_not_found():
<<<<<<< HEAD
    ///Prueba que la ruta '/roluser/{id}' devuelve un error 404 si no se encuentra el tipo de usuario.///
    response = client.get("/roluser/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Not found"}
"""
=======
    """Prueba que la ruta '/roluser/{id}' devuelve un error 404 si no se encuentra el tipo de usuario."""
    response = client.get("/roluser/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Not found"}
>>>>>>> 84f3392 (updating tests)
