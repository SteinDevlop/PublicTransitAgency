import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from fastapi.staticfiles import StaticFiles

from backend.app.api.routes.rol_user_service.rol_user_query_service import app as roluser_router
from backend.app.logic.universal_controller_sqlserver import UniversalController
from backend.app.core.conf import headers
from backend.app.models.rol_user import RolUserOut


test_app = FastAPI()
test_app.include_router(roluser_router)
test_app.mount("/static", StaticFiles(directory="src/frontend/static"), name="static")
client = TestClient(test_app)

# Test GET /consultar (vista HTML)
def test_consultar_page():
    response = client.get("/roluser/administrador/consultar",headers=headers)
    assert response.status_code == 200

def test_read_all():
    """Prueba que la ruta '/user/' devuelve todos los tipos de transporte."""
    response = client.get("/roluser/administrador/rolusers", headers=headers)
    assert response.status_code == 200

def test_get_by_id():
    """Prueba que la ruta '/user/{id}' devuelve el usuario correcto."""
    response = client.get("/roluser/administrador/tipousuario?ID=1", headers=headers)
    assert response.status_code == 200

def test_get_by_id_not_found():
    """Prueba que la ruta '/user/{id}' devuelve un error 404 si no se encuentra el usuario."""
    response = client.get("/roluser/administrador/tipousuario?ID=999", headers=headers)  # ID que no existe
    assert response.status_code == 404
    assert response.json() == {'detail': 'Rol Usuario no encontrado'}

