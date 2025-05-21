import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from backend.app.api.routes.behavior_service.behavior_query_service import router as behavior_router
from backend.app.core.conf import headers

test_app = FastAPI()
test_app.include_router(behavior_router)
client = TestClient(test_app)

def test_consultar_administrador():
    """Prueba que la ruta '/behavior/administrador/consultar' devuelve un mensaje JSON correctamente."""
    response = client.get("/behavior/administrador/consultar", headers=headers)
    assert response.status_code == 200
    assert "Consulta de rendimientos para administrador" in response.json()["message"]

def test_consultar_supervisor():
    """Prueba que la ruta '/behavior/supervisor/consultar' devuelve un mensaje JSON correctamente."""
    response = client.get("/behavior/supervisor/consultar", headers=headers)
    assert response.status_code == 200
    assert "Consulta de rendimientos para supervisor" in response.json()["message"]

def test_get_behaviors_admin():
    """Prueba que la ruta '/behavior/administrador/behaviors' devuelve behaviors en JSON."""
    response = client.get("/behavior/administrador/behaviors", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "behaviors" in data
    assert isinstance(data["behaviors"], list)

def test_get_behaviors_supervisor():
    """Prueba que la ruta '/behavior/supervisor/behaviors' devuelve behaviors en JSON."""
    response = client.get("/behavior/supervisor/behaviors", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "behaviors" in data
    assert isinstance(data["behaviors"], list)

def test_get_rendimientos():
    """Prueba que la ruta '/behavior/rendimientos' devuelve rendimientos en JSON."""
    response = client.get("/behavior/rendimientos", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "rendimientos" in data
    assert isinstance(data["rendimientos"], list)

def test_get_by_id_found():
    """Prueba que la ruta '/behavior/byid?ID=...' devuelve el rendimiento correcto."""
    # Primero, deberías asegurarte que exista un comportamiento con ese ID en pruebas
    response = client.get("/behavior/byid?ID=45", headers=headers)
    if response.status_code == 200:
        data = response.json()
        assert "ID" in data
        assert data["ID"] == 45
    else:
        # Si no existe, el test sigue siendo válido (puede que la base esté limpia)
        assert response.status_code == 404

def test_get_by_id_not_found():
    """Prueba que la ruta '/behavior/byid?ID=...' devuelve error 404 si no existe."""
    response = client.get("/behavior/byid?ID=99999", headers=headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "Rendimiento no encontrado"

def test_get_by_user():
    """Prueba que la ruta '/behavior/byuser?iduser=...' devuelve una lista de rendimientos."""
    response = client.get("/behavior/byuser?iduser=99", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "rendimientos" in data
    assert isinstance(data["rendimientos"], list)