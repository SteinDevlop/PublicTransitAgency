import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from fastapi.staticfiles import StaticFiles

from backend.app.api.routes.price_service.price_query_service import router as price_router
from backend.app.core.conf import headers

test_app = FastAPI()
test_app.include_router(price_router)
test_app.mount("/static", StaticFiles(directory="src/frontend/static"), name="static")
client = TestClient(test_app)

def test_consultar_page():
    """Prueba que la ruta '/price/administrador/consultar' responde con un mensaje JSON."""
    response = client.get("/price/administrador/consultar", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "precio para administrador" in data["message"]

def test_get_prices_admin():
    """Prueba que la ruta '/price/administrador/prices' devuelve todos los precios en JSON."""
    response = client.get("/price/administrador/prices", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "prices" in data
    assert isinstance(data["prices"], list)

def test_get_by_id():
    """Prueba que la ruta '/price/administrador/precio?id=44' devuelve el precio correcto en JSON, o 404 si no existe."""
    response = client.get("/price/administrador/precio?id=44", headers=headers)
    if response.status_code == 200:
        data = response.json()
        assert data["ID"] == 44
        assert "IDTipoTransporte" in data
        assert "Monto" in data
    else:
        assert response.status_code == 404
        assert response.json()["detail"] == "Precio no encontrado"

def test_get_by_id_not_found():
    """Prueba que la ruta '/price/administrador/precio?id=999' devuelve un error 404 si no se encuentra el precio."""
    response = client.get("/price/administrador/precio?id=999", headers=headers)
    assert response.status_code == 404
    assert response.json() == {'detail': 'Precio no encontrado'}