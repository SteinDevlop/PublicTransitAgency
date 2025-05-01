from fastapi import FastAPI
from fastapi.testclient import TestClient
from backend.app.api.routes.schedule_query_service import app as schedule_query_router
import datetime

# Creamos la app de prueba
app_for_test = FastAPI()
app_for_test.include_router(schedule_query_router)

# Cliente de prueba
client = TestClient(app_for_test)

def test_list_schedules_page():
    response = client.get("/schedules/listar")
    assert response.status_code == 200
    assert "ListarHorario" in response.text # Verifica el título o contenido específico de la tabla

def test_schedule_detail_page_existing():
    # Asumimos que existe un horario con ID 'SCH001' en la base de datos de prueba
    response = client.get("/schedules/detalles/SCH001")
    assert response.status_code == 200
    assert "DetalleHorario" in response.text # Verifica el título o contenido específico de la página de detalles

def test_schedule_detail_page_not_found():
    response = client.get("/schedules/detalles/NONEXISTENT")
    assert response.status_code == 404
    assert "Horario no encontrado" in response.text

def test_get_all_schedules():
    response = client.get("/schedules/all")
    assert response.status_code == 200
    assert isinstance(response.json(), list) # Verifica que la respuesta sea una lista

def test_get_schedule_by_id_existing():
    # Asumimos que existe un horario con ID 'SCH002' en la base de datos de prueba
    response = client.get("/schedules/SCH002")
    assert response.status_code == 200
    assert response.json()["schedule_id"] == "SCH002"

def test_get_schedule_by_id_not_found():
    response = client.get("/schedules/NONEXISTENT")
    assert response.status_code == 404
    assert response.json()["detail"] == "Schedule not found"