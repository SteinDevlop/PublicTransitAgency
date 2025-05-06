import pytest
from fastapi.testclient import TestClient
from backend.app.api.routes.schedule_cud_service import app
from backend.app.models.schedule import Schedule
from backend.app.logic.universal_controller_postgres import UniversalController
from backend.app.core.conf import headers  # Importar el token de conf.py

client = TestClient(app)
controller = UniversalController()

@pytest.fixture(scope="function", autouse=True)
def limpiar_tabla():
    controller.clear_tables()  # Limpiar la tabla antes y después de cada prueba
    yield
    controller.clear_tables()

def test_crear_horario():
    response = client.post("/schedules/create", data={
        "id": 1,
        "llegada": "08:00:00",
        "salida": "10:00:00"
    }, headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Horario creado exitosamente."
    assert response.json()["data"]["id"] == 1
    assert response.json()["data"]["llegada"] == "08:00:00"
    assert response.json()["data"]["salida"] == "10:00:00"

def test_actualizar_horario():
    controller.add(Schedule(id=1, llegada="08:00:00", salida="10:00:00"))
    response = client.post("/schedules/update", data={
        "id": 1,
        "llegada": "09:00:00",
        "salida": "11:00:00"
    }, headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Horario actualizado exitosamente."
    updated_schedule = response.json()["data"]
    assert updated_schedule["id"] == 1
    assert updated_schedule["llegada"] == "09:00:00"
    assert updated_schedule["salida"] == "11:00:00"

def test_eliminar_horario():
    controller.add(Schedule(id=1, llegada="08:00:00", salida="10:00:00"))
    response = client.post("/schedules/delete", data={"id": 1}, headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Horario eliminado exitosamente."

def test_eliminar_horario_inexistente():
    response = client.post("/schedules/delete", data={"id": 1}, headers=headers)
    assert response.status_code == 404
    assert "Horario no encontrado" in response.json()["detail"]

def test_actualizar_horario_inexistente():
    response = client.post("/schedules/update", data={
        "id": 1,
        "llegada": "09:00:00",
        "salida": "11:00:00"
    }, headers=headers)
    assert response.status_code == 404
    assert "Horario no encontrado" in response.json()["detail"]