import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from backend.app.api.routes.price_query_service import app as price_router
from backend.app.logic.universal_controller_sql import UniversalController
from backend.app.models.price import PriceOut


def setup_function():
    UniversalController().clear_tables()

def teardown_function():
    UniversalController().clear_tables()

# Mock para UniversalController
class MockUniversalController:
    def __init__(self):
        # Datos simulados de precios
        self.prices = {
            3: PriceOut(
                id=3,
                unidadtransportype="bus",
                amount=100.0,
                ),
        }

    def read_all(self, model):
        """Simula obtener todos los precios"""
        return list(self.prices.values())

    def get_by_id(self, model, id_: int):
        """Simula obtener un precios por ID"""
        return self.prices.get(id_)

# Patching el controller en tests
@pytest.fixture(autouse=True)
def override_controller(monkeypatch):
    """Fixture para reemplazar el controlador real por el mock"""
    from backend.app.api.routes.price_query_service import controller
    monkeypatch.setattr(controller, "read_all", MockUniversalController().read_all)
    monkeypatch.setattr(controller, "get_by_id", MockUniversalController().get_by_id)

test_app = FastAPI()
test_app.include_router(price_router)
client = TestClient(test_app)

# Test GET /consultar (vista HTML)

def test_read_all():
    """Prueba que la ruta '/price/' devuelve todos los tipos de transporte."""
    response = client.get("/price/prices/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == 3
    assert data[0]["unidadtransportype"] == "bus"
    assert data[0]["amount"] == 100.0

def test_get_by_id():
    """Prueba que la ruta '/price/{id}' devuelve el precio correcto."""
    response = client.get("/price/3")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 3
    assert data["unidadtransportype"] == "bus"
    assert data["amount"] == 100.0

def test_get_by_id_not_found():
    """Prueba que la ruta '/price/{id}' devuelve un error 404 si no se encuentra el precio."""
    response = client.get("/price/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Not found"}

