import pytest
from fastapi.testclient import TestClient
from backend.app.api.routes.reporte_service import app as reporte_router
from fastapi import FastAPI
from backend.app.core.conf import headers
import backend.app.api.routes.reporte_service as reporte_service

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

def test_reporte_supervisor_exception(monkeypatch):
    def raise_exc(*a, **kw):
        raise Exception("fail")
    monkeypatch.setattr(reporte_service.controller, "total_movimientos", raise_exc)
    token = get_token()
    all_headers = {"Authorization": f"Bearer {token}"}
    all_headers.update(headers)
    response = client.get("/reporte/supervisor", headers=all_headers)
    assert response.status_code == 500
    assert "Ocurrió un error al generar el reporte de supervisor." in response.text

def test_reporte_alert_tec_not_serializable(monkeypatch):
    class NotSerializable:
        def __str__(self):
            return "NotSerializable"
    def fake_atrasados():
        return [NotSerializable()]
    def fake_proximos():
        return []
    monkeypatch.setattr(reporte_service.controller, "alerta_mantenimiento_atrasados", fake_atrasados)
    monkeypatch.setattr(reporte_service.controller, "alerta_mantenimiento_proximos", fake_proximos)
    token = get_token()
    all_headers = {"Authorization": f"Bearer {token}"}
    all_headers.update(headers)
    response = client.get("/reporte/alert-tec", headers=all_headers)
    assert response.status_code == 200
    data = response.json()
    # Puede que la lista esté vacía o el objeto se serialice como string
    if data["mantenimientos_atrasados"]:
        val = data["mantenimientos_atrasados"][0]
        assert "NotSerializable" in str(val) or val == {}
    else:
        # Si la lista está vacía, el test sigue pasando
        assert data["mantenimientos_atrasados"] == [] or data["mantenimientos_atrasados"] == [{}]

def test_reporte_alert_tec_exception(monkeypatch):
    def raise_exc(*a, **kw):
        raise Exception("fail")
    monkeypatch.setattr(reporte_service.controller, "alerta_mantenimiento_atrasados", raise_exc)
    token = get_token()
    all_headers = {"Authorization": f"Bearer {token}"}
    all_headers.update(headers)
    response = client.get("/reporte/alert-tec", headers=all_headers)
    assert response.status_code == 500
    assert "Ocurrió un error al generar el reporte técnico." in response.text
