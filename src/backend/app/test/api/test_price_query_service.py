import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from backend.app.api.routes.price_query_service import app as price_router
from backend.app.logic.universal_controller_postgres import UniversalController
from backend.app.core.conf import headers
from backend.app.models.price import PriceOut


def setup_function():
    UniversalController().clear_tables()

def teardown_function():
    UniversalController().clear_tables()

# Mock para UniversalController
class MockUniversalController:
    def __init__(self):
        # Datos simulados de precio
        self.prices = {
            3: PriceOut(
                    id=3,
                    unidadtransportype=1,
                    amount=300
                ),
        }

    def read_all(self, model):
        """Simula obtener todos los usuarios"""
        return list(self.prices.values())

    def get_by_id(self, model, id_: int):
        """Simula obtener un usuario por ID"""
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
#def test_consultar_page():
"""Prueba que la ruta '/consultar' devuelve la plantilla 'ConsultarTarjeta.html' correctamente."""
    #response = client.get("/price/consultar",headers=headers)
    #assert response.status_code == 200
    #assert "Consultar Saldo" in response.text  # Verifica si la plantilla está presente

def test_read_all():
    """Prueba que la ruta '/user/' devuelve todos los tipos de transporte."""
    response = client.get("/price/prices/", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == 3
    assert data[0]["unidadtransportype"] == 1
    assert data[0]["amount"] == 300

def test_get_by_id():
    """Prueba que la ruta '/price/{id}' devuelve el precio correcto."""
    response = client.get("/price/3", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 3
    assert data["unidadtransportype"] == 1
    assert data["amount"] == 300

def test_get_by_id_not_found():
    """Prueba que la ruta '/price/{id}' devuelve un error 404 si no se encuentra el usuario."""
    response = client.get("/price/999", headers=headers)  # ID que no existe
    assert response.status_code == 404
    assert response.json() == "Precio no encontrado"

