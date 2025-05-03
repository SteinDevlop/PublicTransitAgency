from fastapi.testclient import TestClient
from backend.app.api.routes.shifts_query_service import app as shifts_router
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

def test_listar_turnos():
    controller.add(Shift(ID=1, TipoTurno="Diurno"))
    response = client.get("/shifts/")
    assert response.status_code == 200
    assert "Diurno" in response.text

def test_detalle_turno_existente():
    controller.add(Shift(ID=1, TipoTurno="Diurno"))
    response = client.get("/shifts/1")
    assert response.status_code == 200
    assert "Diurno" in response.text

def test_detalle_turno_no_existente():
    response = client.get("/shifts/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Turno no encontrado"



"""
from fastapi.testclient import TestClient
from backend.app.api.routes.shifts_query_service import app as shifts_router
from backend.app.logic.universal_controller_sql import UniversalController
from backend.app.models.shift import ShiftOut
from fastapi import FastAPI

app_for_test = FastAPI()
app_for_test.include_router(shifts_router)
client = TestClient(app_for_test)
controller = UniversalController()

def setup_function():
    controller.clear_tables()

def teardown_function():
    controller.clear_tables()

def test_listar_turnos():
    controller.add(ShiftOut(shift_id="1", unit_id="U1", start_time="2023-05-01T08:00:00", end_time="2023-05-01T16:00:00", driver_id="D1", schedule_id="S1"))
    response = client.get("/shifts/")
    assert response.status_code == 200
    assert "U1" in response.text

def test_detalle_turno_existente():
    controller.add(ShiftOut(shift_id="1", unit_id="U1", start_time="2023-05-01T08:00:00", end_time="2023-05-01T16:00:00", driver_id="D1", schedule_id="S1"))
    response = client.get("/shifts/1")
    assert response.status_code == 200
    assert "U1" in response.text

def test_detalle_turno_no_existente():
    response = client.get("/shifts/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Turno no encontrado"
    """