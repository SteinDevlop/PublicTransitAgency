import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from backend.app.api.routes.behavior_query_service import app as behavior_router
from backend.app.logic.universal_controller_sqlserver import UniversalController
from backend.app.core.conf import headers
from backend.app.models.behavior import BehaviorOut

test_app = FastAPI()
test_app.include_router(behavior_router)
client = TestClient(test_app)

# Test GET /consultar (vista HTML)
#def test_consultar_page():
"""Prueba que la ruta '/consultar' devuelve la plantilla 'ConsultarTarjeta.html' correctamente."""
    #response = client.get("/behavior/consultar",headers=headers)
    #assert response.status_code == 200
    #assert "Consultar Saldo" in response.text  # Verifica si la plantilla está presente

def test_read_all():
    response = client.get("/behavior/rendimientos/", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == 1

def test_get_by_id():
    """Prueba que la ruta '/behavior/{id}' devuelve el behavior correcto."""
    response = client.get("/behavior/1", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1

def test_get_by_userid():
    """Prueba que la ruta '/behavior/user/{iduser}' devuelve las rendimientos correctas para un iduser."""
    response = client.get("/behavior/user/100001", headers=headers)
    assert response.status_code == 200
    
    data = response.json()
    
    # Verificar que la respuesta es una lista de rendimientos
    assert isinstance(data, list)
    
    # Verificar que al menos una asistencia está presente en la respuesta
    assert len(data) > 0
    
    # Verificar que la primera asistencia tiene los campos esperados
    assert "id" in data[0]
    assert "cantidadrutas" in data[0]
    assert "horastrabajadas" in data[0]
    assert "iduser" in data[0]
    assert "fecha" in data[0]
    
    # Opcional: Verificar que la primera asistencia tiene los valores correctos (ajusta según tu base de datos)
    assert data[0]["id"] == 44
    assert data[0]["iduser"] == 100001  # Asume que este es el iduser que buscas

def test_get_by_id_not_found():
    """Prueba que la ruta '/behavior/{id}' devuelve un error 404 si no se encuentra el usuario."""
    response = client.get("/behavior/999", headers=headers)  # ID que no existe
    assert response.status_code == 404
    assert response.json() == {'detail': 'Not Found'}

