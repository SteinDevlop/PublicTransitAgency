import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from fastapi.staticfiles import StaticFiles
from datetime import datetime
from backend.app.api.routes.maintainance_service import maintance_query_service
from backend.app.logic.universal_controller_sql import UniversalController
from backend.app.models.maintainance import MaintenanceCreate
from backend.app.core.conf import headers

# Test setup

# Create a test controller instance
test_controller = UniversalController()
maintance_query_service.controller = test_controller

def setup_function():
    test_controller.clear_tables()

def teardown_function():
    test_controller.clear_tables()

# Create test app
app_for_test = FastAPI()
app_for_test.include_router(maintance_query_service.app)
app_for_test.mount("/static", StaticFiles(directory="src/frontend/static"), name="static")
client = TestClient(app_for_test)



# Test: Get maintenance by ID (success)

def test_get_maintainment_by_id_success():
    test_controller.add(MaintenanceCreate(ID=1, idunidad=1, id_status=2, type="Preventive", fecha=datetime.fromisoformat("2024-01-01T00:00:00")))
    response = client.get("/maintainance/id/1", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["ID"] == 1

# Test: Get maintenance by unit (success)

def test_get_maintainments_by_unit_success():
    test_controller.add(MaintenanceCreate(ID=1, idunidad=1, id_status=1, type="Preventive", fecha=datetime.fromisoformat("2024-01-01T00:00:00")))
    response = client.get("/maintainance/unit/?idunidad=1", headers=headers)
    assert response.status_code == 200
    data = response.json()

# Test: Get maintenance by unit (no results)

def test_get_maintainments_by_unit_no_results():
    response = client.get("/maintainance/unit/?idunidad=999", headers=headers)
    assert response.status_code == 404
    assert response.json() == {"detail": "Not found"}

def test_read_all_success():
    test_controller.add(MaintenanceCreate(ID=2, idunidad=2, id_status=1, type="Corrective", fecha=datetime.fromisoformat("2024-01-02T00:00:00")))
    response = client.get("/maintainance/maintainancements", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert any(m["ID"] == 2 for m in data)

def test_read_all_exception(monkeypatch):
    def raise_exc(*a, **kw):
        raise Exception("fail")
    monkeypatch.setattr(test_controller, "read_all", raise_exc)
    response = client.get("/maintainance/maintainancements", headers=headers)
    assert response.status_code == 500
    assert response.json()["detail"] == "Internal server error"

def test_get_by_id_not_found():
    response = client.get("/maintainance/id/999", headers=headers)
    assert response.status_code == 404
    assert response.json() == {"detail": "Not found"}

def test_listar_mantenimientos_success():
    test_controller.add(MaintenanceCreate(ID=3, idunidad=3, id_status=1, type="Preventive", fecha=datetime.fromisoformat("2024-01-03T00:00:00")))
    response = client.get("/maintainance/listar", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert any(m["ID"] == 3 for m in data)

def test_listar_mantenimientos_exception(monkeypatch):
    def raise_exc(*a, **kw):
        raise Exception("fail")
    monkeypatch.setattr(test_controller, "read_all", raise_exc)
    response = client.get("/maintainance/listar", headers=headers)
    assert response.status_code == 500
    assert "Error al listar mantenimientos" in response.json()["detail"]
