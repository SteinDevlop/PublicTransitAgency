from fastapi import FastAPI
from fastapi.testclient import TestClient
from backend.app.api.routes.schedule_cud_service import app as schedule_cud_router

# Creamos la app de prueba
app_for_test = FastAPI()
app_for_test.include_router(schedule_cud_router)

# Cliente de prueba
client = TestClient(app_for_test)

def test_index_create():
    response = client.get("/schedules/crear")
    assert response.status_code == 200
    assert "CrearHorario" in response.text # Verifica el título o contenido específico del formulario

def test_index_update():
    response = client.get("/schedules/actualizar")
    assert response.status_code == 200
    assert "ActualizarHorario" in response.text # Verifica el título o contenido específico del formulario

def test_index_delete():
    response = client.get("/schedules/eliminar")
    assert response.status_code == 200
    assert "EliminarHorario" in response.text # Verifica el título o contenido específico del formulario

def test_create_schedule():
    response = client.post(
        "/schedules/create",
        data={"schedule_id": "SCH001", "arrival_date": "2025-05-02T08:00:00", "departure_date": "2025-05-02T17:00:00", "route_id": "RUT005"}
    )
    assert response.status_code == 200
    assert response.json()["operation"] == "create"
    assert response.json()["success"] is True
    assert response.json()["data"]["schedule_id"] == "SCH001"
    assert response.json()["data"]["route_id"] == "RUT005"

def test_create_schedule_value_error():
    # Prueba un posible ValueError si la fecha tiene un formato incorrecto
    response = client.post(
        "/schedules/create",
        data={"schedule_id": "SCH002", "arrival_date": "invalid-date", "departure_date": "2025-05-02T18:00:00", "route_id": "RUT006"}
    )
    assert response.status_code == 400
    assert "value is not a valid datetime" in response.json()["detail"] # Ajusta según tu error

def test_update_schedule_existing():
    # Primero crea un horario para actualizarlo
    client.post(
        "/schedules/create",
        data={"schedule_id": "SCH003", "arrival_date": "2025-05-03T09:00:00", "departure_date": "2025-05-03T18:30:00", "route_id": "RUT007"}
    )
    response = client.post(
        "/schedules/update/SCH003",
        data={"arrival_date": "2025-05-03T10:00:00", "departure_date": "2025-05-03T19:00:00", "route_id": "RUT008"}
    )
    assert response.status_code == 200
    assert response.json()["operation"] == "update"
    assert response.json()["success"] is True
    assert response.json()["data"]["schedule_id"] == "SCH003"
    assert response.json()["data"]["arrival_date"] == "2025-05-03T10:00:00"
    assert response.json()["data"]["route_id"] == "RUT008"

def test_update_schedule_not_found():
    response = client.post(
        "/schedules/update/NONEXISTENT",
        data={"arrival_date": "2025-05-04T11:00:00", "departure_date": "2025-05-04T20:00:00", "route_id": "RUT009"}
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Schedule not found"

def test_delete_schedule_existing():
    # Primero crea un horario para eliminarlo
    client.post(
        "/schedules/create",
        data={"schedule_id": "SCH004", "arrival_date": "2025-05-05T12:00:00", "departure_date": "2025-05-05T21:00:00", "route_id": "RUT010"}
    )
    response = client.post("/schedules/delete/SCH004")
    assert response.status_code == 200
    assert response.json()["operation"] == "delete"
    assert response.json()["success"] is True
    assert response.json()["message"] == "Schedule SCH004 deleted successfully"

def test_delete_schedule_not_found():
    response = client.post("/schedules/delete/NONEXISTENT")
    assert response.status_code == 404
    assert response.json()["detail"] == "Schedule not found"