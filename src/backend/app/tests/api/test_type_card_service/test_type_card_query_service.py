import pytest
from fastapi.testclient import TestClient
from backend.app.models.type_card import TypeCardOut
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from backend.app.api.routes.type_card_service.type_card_query_service import app as typecard_router
from backend.app.logic.universal_controller_sql import UniversalController
from backend.app.core.conf import headers
def setup_function():
    UniversalController().clear_tables()

def teardown_function():
    UniversalController().clear_tables()
# Mock de la clase UniversalController
class MockUniversalController:
    def __init__(self):
        # Datos simulados de tipos de tarjeta
        self.typecards = {
            3: TypeCardOut(ID=3, Tipo="lolu"),  # Tipo de tarjeta con ID=3
        }

    def read_all(self, model):
        """Simula obtener todos los tipos de tarjeta"""
        return list(self.typecards.values())

    def get_by_id(self, model, id_: int):
        """Simula obtener un tipo de tarjeta por ID"""
        return self.typecards.get(id_)

@pytest.fixture(autouse=True)
def override_controller(monkeypatch):
    """Fixture para reemplazar el controlador real por el mock"""
    from backend.app.api.routes.type_card_service.type_card_query_service import controller
    monkeypatch.setattr(controller, "read_all", MockUniversalController().read_all)
    monkeypatch.setattr(controller, "get_by_id", MockUniversalController().get_by_id)

# Crear la aplicación de prueba
app_for_test = FastAPI()
app_for_test.include_router(typecard_router)
app_for_test.mount("/static", StaticFiles(directory="src/frontend/static"), name="static")
client = TestClient(app_for_test)

def test_read_all():
    """Prueba que la ruta '/typecards/' devuelve todos los tipos de tarjeta."""
    response = client.get("/typecard/typecards/",headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["ID"] == 3
    assert data[0]["Tipo"] == "lolu"

def test_get_by_id():
    """Prueba que la ruta '/typecard/{ID}' devuelve el tipo de tarjeta correcto."""
    response = client.get("/typecard/3",headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["ID"] == 3
    assert data["Tipo"] == "lolu"

def test_get_by_id_not_found():
    """Prueba que la ruta '/typecard/{ID}' devuelve un error 404 si no se encuentra el tipo de tarjeta."""
    response = client.get("/typecard/999",headers=headers)
    assert response.status_code == 404
    assert response.json() == {"detail": "TypeCard not found"}
