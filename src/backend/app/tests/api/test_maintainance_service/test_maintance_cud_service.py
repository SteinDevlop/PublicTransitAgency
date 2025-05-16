import pytest
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.testclient import TestClient
from backend.app.api.routes.maintainance_service.maintance_cud_service import app as maintance_cud_service
from backend.app.logic.universal_controller_sql import UniversalController
from backend.app.core.conf import headers

test_controller = UniversalController()
maintance_cud_service.controller = test_controller
def setup_function():
    UniversalController().clear_tables()

def teardown_function():
    UniversalController().clear_tables()
# Usamos el app del router
app_for_test = FastAPI()
app_for_test.include_router(maintance_cud_service)
app_for_test.mount("/static", StaticFiles(directory="src/frontend/static"), name="static")
client = TestClient(app_for_test)

# Mock para UniversalController
class MockController:
    def add(self, data):
        return True

    def get_by_id(self, model, ID):
        if ID == 1:
            return {"ID": ID, "idunidad": 1, "id_status": 1, "type": "Preventive", "fecha": "2024-01-01T00:00:00"}
        else:
            return None

    def update(self, data):
        return True

    def delete(self, data):
        return True

# Patching el controller en tests
@pytest.fixture(autouse=True)
def override_controller(monkeypatch):
    from backend.app.api.routes.maintainance_service import maintance_cud_service
    maintance_cud_service.controller = MockController()

# Test POST /create
def test_create_mantainment_post():
    response = client.post("/maintainance/create", data={
        "ID": 1,
        "idunidad": 1,
        "id_status": 2,
        "type": "Preventive",
        "fecha": "2024-01-01T00:00:00"
    },headers=headers)
    assert response.status_code == 200
    assert response.json() == {"message": "Maintenance added successfully"}

# Test POST /update para mantenimiento existente
def test_update_mantainment_post_success():
    response = client.post("/maintainance/update", data={
        "ID": 1,
        "idunidad": 2,
        "id_status": 2,
        "type": "Corrective",
        "fecha": "2024-01-02T00:00:00"
    },headers=headers)
    assert response.status_code == 200
    assert response.json() == {"message": "Maintenance 1 updated successfully"}

# Test POST /update para mantenimiento no encontrado
def test_update_mantainment_post_not_found():
    response = client.post("/maintainance/update", data={
        "ID": 999,  # ID no existente
        "idunidad": 2,
        "id_status": 2,
        "type": "Corrective",
        "fecha": "2024-01-02T00:00:00"
    },headers=headers)
    assert response.status_code == 404
    assert response.json() == {"detail": "Maintenance not found"}

# Test POST /delete para mantenimiento existente
def test_delete_mantainment_post_success():
    response = client.post("/maintainance/delete", data={
        "ID": 1,
    },headers=headers)
    assert response.status_code == 200
    assert response.json() == {"message": "Maintenance 1 deleted successfully"}

# Test POST /delete para mantenimiento no encontrado
def test_delete_mantainment_post_not_found():
    response = client.post("/maintainance/delete", data={"ID": 999},headers=headers)
    assert response.status_code == 404
    assert response.json() == {"detail": "Maintenance not found"}
