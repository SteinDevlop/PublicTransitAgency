"""import pytest
from fastapi.testclient import TestClient
from backend.app.models.type_movement import TypeMovementOut
from fastapi import FastAPI
from backend.app.api.routes.type_movement_query_service import app as typemovement_router
from backend.app.logic.universal_controller_sql import UniversalController
def setup_function():
    UniversalController().clear_tables()

def teardown_function():
    UniversalController().clear_tables()
# Mock de la clase UniversalController
class MockUniversalController:
    def __init__(self):
        # Datos simulados de tipos de movimiento
        self.typemovements = {
            3: TypeMovementOut(id=3, type="income"),  # Tipo de movimiento con id=3
            4: TypeMovementOut(id=4, type="expense"),  # Tipo de movimiento con id=4
        }

    def read_all(self, model):
        ///Simula obtener todos los tipos de movimiento///
        return list(self.typemovements.values())

    def get_by_id(self, model, id_: int):
        ///Simula obtener un tipo de movimiento por ID///
        return self.typemovements.get(id_)

@pytest.fixture(autouse=True)
def override_controller(monkeypatch):
    ///Fixture para reemplazar el controlador real por el mock///
    from backend.app.api.routes.type_movement_query_service import controller
    monkeypatch.setattr(controller, "read_all", MockUniversalController().read_all)
    monkeypatch.setattr(controller, "get_by_id", MockUniversalController().get_by_id)

# Crear la aplicación de prueba
app_for_test = FastAPI()
app_for_test.include_router(typemovement_router)

client = TestClient(app_for_test)

def test_read_all():
    ///Prueba que la ruta '/typemovements/' devuelve todos los tipos de movimiento.///
    response = client.get("/typemovement/typemovements/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["id"] == 3
    assert data[0]["type"] == "income"
    assert data[1]["id"] == 4
    assert data[1]["type"] == "expense"

def test_get_by_id():
    ///Prueba que la ruta '/typemovement/{id}' devuelve el tipo de movimiento correcto.///
    response = client.get("/typemovement/4")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 4
    assert data["type"] == "expense"

def test_get_by_id_not_found():
    ///Prueba que la ruta '/typemovement/{id}' devuelve un error 404 si no se encuentra el tipo de movimiento.///
    response = client.get("/typemovement/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Not found"}
"""