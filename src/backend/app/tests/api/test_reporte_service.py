import pytest
from fastapi.testclient import TestClient
from backend.app.api.routes.reporte_service import app as reporte_router
from fastapi import FastAPI
from backend.app.core.conf import headers

app_for_test = FastAPI()
app_for_test.include_router(reporte_router)
client = TestClient(app_for_test)

def get_token():
    # Simula un token válido para pruebas (ajusta según tu sistema de auth real)
    return "testtoken"

def test_reporte_supervisor():
    token = get_token()
    all_headers = {"Authorization": f"Bearer {token}"}
    all_headers.update(headers)
    response = client.get("/reporte/supervisor", headers=all_headers)
    assert response.status_code == 200
    data = response.json()
    assert "total_movimientos" in data
    assert "total_usuarios" in data
    assert "promedio_horas_trabajadas" in data

def test_reporte_alert_tec():
    token = get_token()
    all_headers = {"Authorization": f"Bearer {token}"}
    all_headers.update(headers)
    response = client.get("/reporte/alert-tec", headers=all_headers)
    assert response.status_code == 200
    data = response.json()
    assert "mantenimientos_atrasados" in data
    assert "mantenimientos_proximos" in data
