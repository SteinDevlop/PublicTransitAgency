from fastapi.testclient import TestClient
from backend.app.api.routes.schedule_cud_service import app as schedules_router
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

def test_crear_horario():
    response = client.post("/schedules/create", data={
        "ID": 1,
        "Llegada": "08:00:00",
        "Salida": "10:00:00"
    })
    assert response.status_code == 200

def test_actualizar_horario():
    controller.add(Schedule(ID=1, Llegada="08:00:00", Salida="10:00:00"))
    response = client.post("/schedules/update", data={
        "ID": 1,
        "Llegada": "09:00:00",
        "Salida": "11:00:00"
    })
    assert response.status_code == 200

def test_eliminar_horario():
    controller.add(Schedule(ID=1, Llegada="08:00:00", Salida="10:00:00"))
    response = client.post("/schedules/delete", data={"ID": 1})
    assert response.status_code == 200