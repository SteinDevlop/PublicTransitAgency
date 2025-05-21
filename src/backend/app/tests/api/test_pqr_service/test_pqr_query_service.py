import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from backend.app.api.routes.pqr_service.pqr_query_service import app as pqr_router
from backend.app.logic.universal_controller_sqlserver import UniversalController
from backend.app.core.conf import headers
from backend.app.models.pqr import PQROut

test_app = FastAPI()
test_app.include_router(pqr_router)
client = TestClient(test_app)

def test_read_all():
    """Prueba que la ruta '/administrador/pqrs/' devuelve todos los pqr."""
    response = client.get("/pqr/administrador/pqrs", headers=headers)
    assert response.status_code == 200

def test_get_by_id():
    """Prueba que la ruta '/pqr/{id}' devuelve el pqr correcto."""
    response = client.get("/pqr/find?ID=33", headers=headers)
    assert response.status_code == 200

def test_get_by_userid():
    """Prueba que la ruta '/pqr/user/{iduser}' devuelve el pqr correcto."""
    response = client.get("/pqr/user?iduser=32232", headers=headers)
    assert response.status_code == 200


def test_get_by_id_not_found():
    """Prueba que la ruta '/pqr/{id}' devuelve un error 404 si no se encuentra el usuario."""
    response = client.get("/pqr/find?ID=44", headers=headers)  # ID que no existe
    assert response.status_code == 404

