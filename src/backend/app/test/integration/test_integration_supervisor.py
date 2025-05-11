"""
import pytest
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.testclient import TestClient

# Importación de modelos y controladores
from backend.app.logic.universal_controller_sql import UniversalController
from backend.app.api.routes import shifts_cud_service
from backend.app.api.routes import type_transport_query_service
from backend.app.api.routes import incidence_query_service

from backend.app.core.conf import headers
from backend.app.models.shift import Shift
from backend.app.models.type_transport import TypeTransportCreate
from backend.app.models.incidence import Incidence

# Crear instancia del controlador para pruebas
test_controller = UniversalController()

# Sobrecargar los controladores en los microservicios
shifts_cud_service.controller = test_controller
type_transport_query_service.controller = test_controller
incidence_query_service.controller = test_controller

# Crear la aplicación FastAPI de prueba
app_for_test = FastAPI()
app_for_test.include_router(shifts_cud_service.app)
app_for_test.include_router(type_transport_query_service.app)
app_for_test.include_router(incidence_query_service.app)
app_for_test.mount("/static", StaticFiles(directory="src/frontend/static"), name="static")

client = TestClient(app_for_test)

# Limpieza de la base de datos antes y después de cada prueba
def setup_function():
    test_controller.clear_tables()

def teardown_function():
    test_controller.clear_tables()

# -------------------
# PRUEBAS DE SHIFTS
# -------------------
def test_crear_turno():

    response = client.post("/shifts/create", json={"id": 1, "tipoturno": "Diurno"}, headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Turno creado exitosamente."

# -------------------
# PRUEBAS DE TIPO DE TRANSPORTE
# -------------------

def test_tipo_transporte_no_encontrado():
    test_controller.add(TypeTransportCreate(ID=1, Tipo="Bus"))
    response = client.get("/typetransport/999", headers=headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "Tipo de transporte no encontrado"

# -------------------
# PRUEBAS DE INCIDENCIAS
# -------------------

def test_incidencia_no_encontrada():
    response = client.get("/incidences/999", headers=headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "Incidencia no encontrada"
"""