import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from backend.app.api.routes.movement_service.movement_query_service import router as movement_router
from backend.app.core.conf import headers

test_app = FastAPI()
test_app.include_router(movement_router)
client = TestClient(test_app)

def test_get_all_pasajero_movements(monkeypatch):
    monkeypatch.setattr(
        "backend.app.core.auth.get_current_user",
        lambda *a, **kw: {"user_id": "test_admin"}
    )
    """
    Prueba que la ruta '/movement/pasajero/movements' devuelve un JSON con todos los movimientos.
    """
    response = client.get("/movement/pasajero/movements", headers=headers)
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("application/json")
    assert isinstance(response.json(), list)

def test_get_all_admin_movements(monkeypatch):
    monkeypatch.setattr(
        "backend.app.core.auth.get_current_user",
        lambda *a, **kw: {"user_id": "test_admin"}
    )
    """
    Prueba que la ruta '/movement/administrador/movements' devuelve un JSON con todos los movimientos.
    """
    response = client.get("/movement/administrador/movements", headers=headers)
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("application/json")
    assert isinstance(response.json(), list)

def test_get_movement_by_id_found(monkeypatch):
    monkeypatch.setattr(
        "backend.app.core.auth.get_current_user",
        lambda *a, **kw: {"user_id": "test_admin"}
    )
    """
    Prueba que la ruta '/movement/administrador/byid' devuelve un movimiento correcto en JSON.
    """
    # Puedes cambiar el ID a uno existente en tus fixtures o en la base de datos de test
    response = client.get("/movement/administrador/byid?ID=12190770", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "ID" in data
    assert "IDTipoMovimiento" in data
    assert "Monto" in data
    assert "IDTarjeta" in data

def test_get_movement_by_id_not_found(monkeypatch):
    """
    Prueba que la ruta '/movement/administrador/byid' devuelve 404 si el movimiento no existe.
    """
    monkeypatch.setattr(
        "backend.app.core.auth.get_current_user",
        lambda *a, **kw: {"user_id": "test_admin"}
    )
    response = client.get("/movement/administrador/byid?ID=999999", headers=headers)
    assert response.status_code == 404
    assert response.json()["detail"].startswith("Movimiento con id=")