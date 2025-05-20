import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from fastapi.staticfiles import StaticFiles

from backend.app.api.routes.user_service.user_query_service import app as user_router
from backend.app.logic.universal_controller_sqlserver import UniversalController
from backend.app.core.conf import headers
from backend.app.models.user import UserOut

test_app = FastAPI()
test_app.mount("/static", StaticFiles(directory="src/frontend/static"), name="static")
test_app.include_router(user_router)
client = TestClient(test_app)

# Test GET /consultar (vista HTML)
def test_consultar_page():
    response = client.get("/user/consultar",headers=headers)
    assert response.status_code == 200

def test_read_all():
    """Prueba que la ruta '/user/' devuelve todos los tipos de transporte."""
    response = client.get("/user/users", headers=headers)
    assert response.status_code == 200

def test_get_by_id():
    """Prueba que la ruta '/user/{id}' devuelve el usuario correcto."""
    response = client.get("/user/usuario?id=41", headers=headers)
    assert response.status_code == 200
