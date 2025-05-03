from fastapi.testclient import TestClient
from backend.app.api.routes.schedule_query_service import app as schedules_router
from backend.app.logic.universal_controller_sql import UniversalController
from backend.app.models.schedule import Schedule
from fastapi import FastAPI

app_for_test = FastAPI()
app_for_test.include_router(schedules_router)
client = TestClient(app_for_test)
controller = UniversalController()

def setup_function():
    controller.clear_tables()

def teardown_function():
    controller.clear_tables()

def test_listar_horarios():
    controller.add(Schedule(ID=1, Llegada="08:00:00", Salida="10:00:00"))
    response = client.get("/schedules/")
    assert response.status_code == 200
    assert "08:00:00" in response.text

def test_detalle_horario_existente():
    controller.add(Schedule(ID=1, Llegada="08:00:00", Salida="10:00:00"))
    response = client.get("/schedules/1")
    assert response.status_code == 200
    assert "08:00:00" in response.text

def test_detalle_horario_no_existente():
    response = client.get("/schedules/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Horario no encontrado"