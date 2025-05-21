import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from fastapi.staticfiles import StaticFiles

from backend.app.api.routes.rol_user_service.rol_user_query_service import router as roluser_router
from backend.app.core.conf import headers

test_app = FastAPI()
test_app.include_router(roluser_router)
test_app.mount("/static", StaticFiles(directory="src/frontend/static"), name="static")
client = TestClient(test_app)

def test_consultar_page():
    response = client.get("/roluser/administrador/consultar", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "rol de usuario" in data["message"]

def test_read_all():
    """Prueba que la ruta '/roluser/administrador/rolusers' devuelve todos los roles de usuario en JSON."""
    response = client.get("/roluser/administrador/rolusers", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "rolusers" in data
    assert isinstance(data["rolusers"], list)
    # Puedes ajustar el siguiente assert si conoces la cantidad esperada
    # assert len(data["rolusers"]) == N

def test_get_by_id():
    """Prueba que la ruta '/roluser/administrador/tipousuario?ID=1' devuelve el rol de usuario correcto en JSON, o 404 si no existe."""
    response = client.get("/roluser/administrador/tipousuario?ID=1", headers=headers)
    if response.status_code == 200:
        data = response.json()
        assert data["ID"] == 1
        assert "Rol" in data
    else:
        assert response.status_code == 404
        assert response.json()["detail"] == "Rol Usuario no encontrado"

def test_get_by_id_not_found():
    """Prueba que la ruta '/roluser/administrador/tipousuario?ID=999' devuelve un error 404 si no se encuentra el rol de usuario."""
    response = client.get("/roluser/administrador/tipousuario?ID=999", headers=headers)
    assert response.status_code == 404
    assert response.json() == {'detail': 'Rol Usuario no encontrado'}