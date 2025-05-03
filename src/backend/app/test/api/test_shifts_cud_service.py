from fastapi.testclient import TestClient
from backend.app.api.routes.shifts_CUD_service import app as shifts_router
from backend.app.logic.universal_controller_sql import UniversalController
from backend.app.models.shift import Shift
from fastapi import FastAPI

app_for_test = FastAPI()
app_for_test.include_router(shifts_router)
client = TestClient(app_for_test)
controller = UniversalController()

def setup_function():
    controller.clear_tables()

def teardown_function():
    controller.clear_tables()

def test_crear_turno():
    response = client.post("/shifts/create", data={"ID": 1, "TipoTurno": "Diurno"})
    assert response.status_code == 200

def test_actualizar_turno():
    controller.add(Shift(ID=1, TipoTurno="Diurno"))
    response = client.post("/shifts/update", data={"ID": 1, "TipoTurno": "Nocturno"})
    assert response.status_code == 200

def test_eliminar_turno():
    controller.add(Shift(ID=1, TipoTurno="Diurno"))
    response = client.post("/shifts/delete", data={"ID": 1})
    assert response.status_code == 200

"""
from fastapi.testclient import TestClient
from backend.app.api.routes.shifts_cud_service import app as shifts_router
from backend.app.logic.universal_controller_sql import UniversalController
from backend.app.models.shift import ShiftCreate
from fastapi import FastAPI

app_for_test = FastAPI()
app_for_test.include_router(shifts_router)
client = TestClient(app_for_test)
controller = UniversalController()

def setup_function():
    controller.clear_tables()

def teardown_function():
    controller.clear_tables()

def test_crear_turno():
    response = client.post("/shifts/create", data={
        "shift_id": "1",
        "unit_id": "U1",
        "start_time": "2023-05-01T08:00:00",
        "end_time": "2023-05-01T16:00:00",
        "driver_id": "D1",
        "schedule_id": "S1"
    })
    assert response.status_code == 200

def test_actualizar_turno():
    controller.add(ShiftCreate(shift_id="1", unit_id="U1", start_time="2023-05-01T08:00:00", end_time="2023-05-01T16:00:00", driver_id="D1", schedule_id="S1"))
    response = client.post("/shifts/update", data={
        "shift_id": "1",
        "unit_id": "U2",
        "start_time": "2023-05-01T09:00:00",
        "end_time": "2023-05-01T17:00:00",
        "driver_id": "D2",
        "schedule_id": "S2"
    })
    assert response.status_code == 200

def test_eliminar_turno():
    controller.add(ShiftCreate(shift_id="1", unit_id="U1", start_time="2023-05-01T08:00:00", end_time="2023-05-01T16:00:00", driver_id="D1", schedule_id="S1"))
    response = client.post("/shifts/delete", data={"shift_id": "1"})
    assert response.status_code == 200
    """