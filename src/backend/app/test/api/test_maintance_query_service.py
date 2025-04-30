import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from backend.app.api.routes.maintance_query_service import app as maintainance_query_router
from backend.app.logic.universal_controller_sql import UniversalController
def setup_function():
    UniversalController().clear_tables()

def teardown_function():
    UniversalController().clear_tables()
# Creamos una app de prueba e incluimos el router
app_for_test = FastAPI()
app_for_test.include_router(maintainance_query_router)

client = TestClient(app_for_test)

# Mock para el Controller
class MockControllerMaintenance:
    def get_all(self):
        return [
            {"id": 1, "id_unit": 1, "id_status": 1, "type": "Preventive", "date": "2024-01-01T00:00:00"},
            {"id": 2, "id_unit": 2, "id_status": 2, "type": "Corrective", "date": "2024-01-02T00:00:00"},
        ]

    def get_by_id(self, id):
        if id == 1:
            class MockMaintenance:
                def to_dict(self):
                    return {"id": 1, "id_unit": 1, "id_status": 1, "type": "Preventive", "date": "2024-01-01T00:00:00"}
            return MockMaintenance()
        else:
            return None

    def get_by_unit(self, unit_id):
        if unit_id == 1:
            return [
                {"id": 1, "id_unit": 1, "id_status": 1, "type": "Preventive", "date": "2024-01-01T00:00:00"}
            ]
        else:
            return []

# Patching automático usando fixture
@pytest.fixture(autouse=True)
def override_controller(monkeypatch):
    from backend.app.api.routes import maintance_query_service
    maintance_query_service.controller_maintenance = MockControllerMaintenance()

# Test GET /maintainancements
def test_get_all_maintainments():
    response = client.get("/maintainance/maintainancements")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["type"] == "Preventive"

# Test GET /{id} para mantenimiento existente
def test_get_maintainment_by_id_success():
    response = client.get("/maintainance/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["type"] == "Preventive"

# Test GET /{id} para mantenimiento no existente
def test_get_maintainment_by_id_not_found():
    response = client.get("/maintainance/9999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Not found"}

# Test GET /unit/{unit_id} con resultados
def test_get_maintainments_by_unit_success():
    response = client.get("/maintainance/unit/1")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["id_unit"] == 1

# Test GET /unit/{unit_id} sin resultados
def test_get_maintainments_by_unit_no_results():
    response = client.get("/maintainance/unit/9999")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 0
