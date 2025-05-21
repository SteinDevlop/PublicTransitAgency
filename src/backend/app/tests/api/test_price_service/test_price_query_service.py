import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from fastapi.staticfiles import StaticFiles

from backend.app.api.routes.price_service.price_query_service import app as price_router
from backend.app.logic.universal_controller_sqlserver import UniversalController
from backend.app.core.conf import headers
from backend.app.models.price import PriceOut

test_app = FastAPI()
test_app.include_router(price_router)
test_app.mount("/static", StaticFiles(directory="src/frontend/static"), name="static")
client = TestClient(test_app)

# Test GET /consultar (vista HTML)
def test_consultar_page():
    """Prueba que la ruta '/consultar' devuelve la plantilla 'ConsultarTarjeta.html' correctamente."""
    response = client.get("/price/administrador/consultar",headers=headers)
    assert response.status_code == 200

def test_get_by_id():
    """Prueba que la ruta '/price/{id}' devuelve el precio correcto."""
    response = client.get("/price/administrador/precio?id=44", headers=headers)
    assert response.status_code == 200

def test_get_by_id_not_found():
    """Prueba que la ruta '/price/{id}' devuelve un error 404 si no se encuentra el usuario."""
    response = client.get("/price/administrador/precio?id=999", headers=headers)  # ID que no existe
    assert response.status_code == 404
    assert response.json() == {'detail': 'Precio no encontrado'}

