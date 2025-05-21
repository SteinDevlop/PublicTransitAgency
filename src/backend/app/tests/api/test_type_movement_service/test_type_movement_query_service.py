import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from fastapi.staticfiles import StaticFiles

from backend.app.api.routes.type_movement_service.type_movement_query_service import router as typemovement_router
from backend.app.core.conf import headers

test_app = FastAPI()
test_app.include_router(typemovement_router)
test_app.mount("/static", StaticFiles(directory="src/frontend/static"), name="static")
client = TestClient(test_app)

def test_consultar_page():
    """Prueba que la ruta '/consultar' devuelve un mensaje JSON de consulta."""
    response = client.get("/typemovement/consultar", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "tipo de movimiento" in data["message"]

def test_read_all():
    """Prueba que la ruta '/typemovement/typemovements' devuelve todos los tipos de movimiento en JSON."""
    response = client.get("/typemovement/typemovements", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "typemovements" in data
    assert isinstance(data["typemovements"], list)
    # Puedes ajustar el siguiente assert si tienes una cantidad esperada
    # assert len(data["typemovements"]) == N

def test_get_by_id():
    """Prueba que la ruta '/typemovement/tipomovimiento?id=2' devuelve el tipo de movimiento correcto en JSON, o 404 si no existe."""
    response = client.get("/typemovement/tipomovimiento?id=2", headers=headers)
    if response.status_code == 200:
        data = response.json()
        assert data["ID"] == 2
        assert "TipoMovimiento" in data
    else:
        assert response.status_code == 404
        assert response.json()["detail"] == "Tipo de movimiento no encontrado"

def test_get_by_id_not_found():
    """Prueba que la ruta '/typemovement/tipomovimiento?id=999' devuelve un error 404 si no se encuentra el tipo de movimiento."""
    response = client.get("/typemovement/tipomovimiento?id=999", headers=headers)
    assert response.status_code == 404
    assert response.json() == {"detail": "Tipo de movimiento no encontrado"}