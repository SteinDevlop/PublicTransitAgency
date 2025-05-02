import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from backend.app.api.routes.movement_query_service import app as movement_router
from backend.app.logic.universal_controller_sql import UniversalController
from backend.app.models.movement import MovementOut


def setup_function():
    UniversalController().clear_tables()

def teardown_function():
    UniversalController().clear_tables()

# Mock para UniversalController
class MockUniversalController:
    def __init__(self):
        # Datos simulados de precios
        self.movements = {
            3: MovementOut(
                id=3,
                type="income",
                amount=100.0,
                ),
        }

    def read_all(self, model):
        """Simula obtener todos los movimientos"""
        return list(self.movements.values())

    def get_by_id(self, model, id_: int):
        """Simula obtener un movimiento por ID"""
        return self.movements.get(id_)

# Patching el controller en tests
@pytest.fixture(autouse=True)
def override_controller(monkeypatch):
    """Fixture para reemplazar el controlador real por el mock"""
    from backend.app.api.routes.movement_query_service import controller
    monkeypatch.setattr(controller, "read_all", MockUniversalController().read_all)
    monkeypatch.setattr(controller, "get_by_id", MockUniversalController().get_by_id)

test_app = FastAPI()
test_app.include_router(movement_router)
client = TestClient(test_app)

# Test GET /consultar (vista HTML)

def test_read_all():
    """Prueba que la ruta '/movement/' devuelve todos los movimientos."""
    response = client.get("/movement/movements/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == 3
    assert data[0]["type"] == "income"
    assert data[0]["amount"] == 100.0

def test_get_by_id():
    """Prueba que la ruta '/movement/{id}' devuelve el movimiento correcto."""
    response = client.get("/movement/3")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 3
    assert data["type"] == "income"
    assert data["amount"] == 100.0

def test_get_by_id_not_found():
    """Prueba que la ruta '/movement/{id}' devuelve un error 404 si no se encuentra el movimiento."""
    response = client.get("/movement/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Not found"}