import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from backend.app.api.routes.pqr_service.pqr_query_service import router as pqr_router
from backend.app.core.conf import headers

test_app = FastAPI()
test_app.include_router(pqr_router)
client = TestClient(test_app)

def test_read_all():
    """Prueba que la ruta '/pqr/administrador/pqrs' devuelve todos los pqr en JSON."""
    response = client.get("/pqr/administrador/pqrs", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "pqrs" in data
    assert isinstance(data["pqrs"], list)

def test_get_by_id():
    """Prueba que la ruta '/pqr/find?ID=33' devuelve el pqr correcto o 404 si no existe."""
    response = client.get("/pqr/find?ID=33", headers=headers)
    if response.status_code == 200:
        data = response.json()
        assert data["ID"] == 33
        assert "type" in data
        assert "description" in data
        assert "fecha" in data
        assert "identificationuser" in data
    else:
        # Si no existe, debe responder 404, el siguiente test lo cubre
        assert response.status_code == 404
        assert response.json()["detail"] == "PQR not found"

def test_get_by_userid():
    """Prueba que la ruta '/pqr/user?iduser=32232' devuelve el pqr correcto o 404 si no existe."""
    response = client.get("/pqr/user?iduser=32232", headers=headers)
    if response.status_code == 200:
        # Puede devolver un dict o una lista de pqr dicts
        data = response.json()
        if isinstance(data, dict) and "pqrs" in data:
            # Lista de PQRs
            assert isinstance(data["pqrs"], list)
            for item in data["pqrs"]:
                assert "ID" in item
                assert "type" in item
                assert "description" in item
                assert "fecha" in item
                assert "identificationuser" in item
        else:
            # Un solo PQR
            assert "ID" in data
            assert "type" in data
            assert "description" in data
            assert "fecha" in data
            assert "identificationuser" in data
    else:
        assert response.status_code == 404
        assert response.json()["detail"] == "PQR not found"

def test_get_by_id_not_found():
    """Prueba que la ruta '/pqr/find?ID=44' devuelve un error 404 si no se encuentra el pqr."""
    response = client.get("/pqr/find?ID=44", headers=headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "PQR not found"