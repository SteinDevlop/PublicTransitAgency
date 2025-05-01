<<<<<<< HEAD
"""import pytest
=======
import pytest
>>>>>>> 84f3392 (updating tests)
from fastapi.testclient import TestClient
from backend.app.models.type_transport import TypeTransportOut
from fastapi import FastAPI
from backend.app.api.routes.type_transport_query_service import app as typetransport_router
from backend.app.logic.universal_controller_sql import UniversalController
def setup_function():
    UniversalController().clear_tables()

def teardown_function():
    UniversalController().clear_tables()
# Mock de la clase UniversalController
class MockUniversalController:
    def __init__(self):
        # Datos simulados de tipos de tarjeta
        self.typetransports = {
            3: TypeTransportOut(id=3, type="bus"),  # Tipo de tarjeta con id=3
        }

    def read_all(self, model):
<<<<<<< HEAD
        ///Simula obtener todos los tipos de transporte///
        return list(self.typetransports.values())

    def get_by_id(self, model, id_: int):
        ///Simula obtener un tipo de transporte por ID///
=======
        """Simula obtener todos los tipos de transporte"""
        return list(self.typetransports.values())

    def get_by_id(self, model, id_: int):
        """Simula obtener un tipo de transporte por ID"""
>>>>>>> 84f3392 (updating tests)
        return self.typetransports.get(id_)

@pytest.fixture(autouse=True)
def override_controller(monkeypatch):
<<<<<<< HEAD
    ///Fixture para reemplazar el controlador real por el mock///
=======
    """Fixture para reemplazar el controlador real por el mock"""
>>>>>>> 84f3392 (updating tests)
    from backend.app.api.routes.type_transport_query_service import controller
    monkeypatch.setattr(controller, "read_all", MockUniversalController().read_all)
    monkeypatch.setattr(controller, "get_by_id", MockUniversalController().get_by_id)

# Crear la aplicación de prueba
app_for_test = FastAPI()
app_for_test.include_router(typetransport_router)

client = TestClient(app_for_test)

def test_read_all():
<<<<<<< HEAD
    ///Prueba que la ruta '/typetransport/' devuelve todos los tipos de transporte.///
=======
    """Prueba que la ruta '/typetransport/' devuelve todos los tipos de transporte."""
>>>>>>> 84f3392 (updating tests)
    response = client.get("/typetransport/typetransports/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == 3
    assert data[0]["type"] == "bus"

def test_get_by_id():
<<<<<<< HEAD
    ///Prueba que la ruta '/typetransport/{id}' devuelve el tipo de transporte correcto.///
=======
    """Prueba que la ruta '/typetransport/{id}' devuelve el tipo de transporte correcto."""
>>>>>>> 84f3392 (updating tests)
    response = client.get("/typetransport/3")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 3
    assert data["type"] == "bus"

def test_get_by_id_not_found():
<<<<<<< HEAD
    ///Prueba que la ruta '/typetransport/{id}' devuelve un error 404 si no se encuentra el tipo de transporte.///
    response = client.get("/typetransport/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Not found"}
"""
=======
    """Prueba que la ruta '/typetransport/{id}' devuelve un error 404 si no se encuentra el tipo de transporte."""
    response = client.get("/typetransport/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Not found"}
>>>>>>> 84f3392 (updating tests)
