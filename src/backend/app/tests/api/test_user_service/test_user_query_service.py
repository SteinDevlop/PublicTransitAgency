import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from fastapi.staticfiles import StaticFiles

from backend.app.api.routes.user_service.user_query_service import router as user_router
from backend.app.core.conf import headers

test_app = FastAPI()
test_app.mount("/static", StaticFiles(directory="src/frontend/static"), name="static")
test_app.include_router(user_router)
client = TestClient(test_app)

def test_consultar_page():
    response = client.get("/user/consultar", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "usuarios" in data["message"]

def test_read_all():
    response = client.get("/user/users", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "usuarios" in data
    assert isinstance(data["usuarios"], list)

def test_get_by_id():
    # Este test asume que existe un usuario con ID=41
    response = client.get("/user/usuario?id=41", headers=headers)
    if response.status_code == 200:
        data = response.json()
        assert data["ID"] == 41
    else:
        # Si no existe, debe retornar 404 y el mensaje adecuado
        assert response.status_code == 404
        assert response.json()["detail"] == "Usuario no encontrado"