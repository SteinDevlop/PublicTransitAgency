import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from fastapi.staticfiles import StaticFiles
from datetime import datetime
from backend.app.api.routes.maintance_query_service import app as maintainance_query_router
from backend.app.logic.universal_controller_sql import UniversalController
from backend.app.models.maintainance import MaintenanceCreate
from backend.app.core.conf import headers

controller = UniversalController()
# Crear instancia de controlador de prueba
maintainance_query_router.controller_maintenance = controller

# Limpieza de BD antes y después de cada test
def setup_function():
    controller.clear_tables()

def teardown_function():
    controller.clear_tables()

# Crear app de prueba e incluir el router
app_for_test = FastAPI()
app_for_test.include_router(maintainance_query_router)
app_for_test.mount("/static", StaticFiles(directory="src/frontend/static"), name="static")

client = TestClient(app_for_test)

# Mock del controlador de mantenimiento


# Test: obtener todos los mantenimientos
def test_get_all_maintainments():
    controller.add(MaintenanceCreate(
        id= 1,
        id_unit=1,
        id_status= 2,
        type= "Preventive",
        fecha= datetime.fromisoformat("2024-01-01T00:00:00")))
    controller.add(MaintenanceCreate(
        id= 2,
        id_unit=1,
        id_status= 2,
        type= "Preventive",
        fecha= datetime.fromisoformat("2024-01-01T00:00:00")))
    response = client.get("/maintainance/maintainancements", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["type"] == "Preventive"

# Test: obtener mantenimiento por ID (existente)
def test_get_maintainment_by_id_success():
    response = client.get("/maintainance/1", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["type"] == "Preventive"

# Test: obtener mantenimiento por ID (no encontrado)
def test_get_maintainment_by_id_not_found():
    response = client.get("/maintainance/9999", headers=headers)
    assert response.status_code == 404
    assert response.json() == {"detail": "Not found"}

# Test: obtener mantenimientos por unidad (con resultados)
def test_get_maintainments_by_unit_success():
    response = client.get("/maintainance/unit/1", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["id_unit"] == 1

# Test: obtener mantenimientos por unidad (sin resultados)
def test_get_maintainments_by_unit_no_results():
    response = client.get("/maintainance/unit/9999", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 0

