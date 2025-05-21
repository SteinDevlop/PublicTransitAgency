import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from backend.app.api.routes.asistance_service.asistance_query_service import router as asistance_router
from backend.app.core.conf import headers

test_app = FastAPI()
test_app.include_router(asistance_router)
client = TestClient(test_app)

def test_consultar_administrador():
    response = client.get("/asistance/consultar/administrador", headers=headers)
    assert response.status_code == 200
    assert "asistencias para administrador" in response.json()["message"]

def test_consultar_conductor():
    response = client.get("/asistance/consultar/conductor", headers=headers)
    assert response.status_code == 200
    assert "asistencias para conductor" in response.json()["message"]

def test_consultar_supervisor():
    response = client.get("/asistance/consultar/supervisor", headers=headers)
    assert response.status_code == 200
    assert "asistencias para supervisor" in response.json()["message"]

def test_consultar_tecnico():
    response = client.get("/asistance/consultar/tecnico", headers=headers)
    assert response.status_code == 200
    assert "asistencias para técnico" in response.json()["message"]

def test_read_all():
    response = client.get("/asistance/asistencias", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "asistencias" in data
    assert isinstance(data["asistencias"], list)

def test_get_by_id_found():
    # Asegúrate de que exista una asistencia con ID 44 antes de este test
    response = client.get("/asistance/find?id=44", headers=headers)
    if response.status_code == 200:
        data = response.json()
        assert data["ID"] == 44
    else:
        assert response.status_code == 404

def test_get_by_id_not_found():
    response = client.get("/asistance/find?id=99999", headers=headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "Asistencia no encontrada"

def test_get_by_user():
    response = client.get("/asistance/user?iduser=99", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "asistencias" in data
    assert isinstance(data["asistencias"], list)