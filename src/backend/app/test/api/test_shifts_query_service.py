import pytest
from fastapi.testclient import TestClient
from backend.app.api.routes.shifts_query_service import app

client = TestClient(app)

def test_list_shifts_page():
    response = client.get("/shifts/listar")
    assert response.status_code == 200
    assert "ListarTurno.html" in response.text

def test_shift_detail_page():
    response = client.get("/shifts/detalles/1")
    if response.status_code == 200:
        assert "DetalleTurno.html" in response.text
    elif response.status_code == 404:
        assert response.json()["detail"] == "Shift not found"

def test_get_all_shifts():
    response = client.get("/shifts/all")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_shift_by_id():
    response = client.get("/shifts/1")
    if response.status_code == 200:
        assert "shift_id" in response.json()
    elif response.status_code == 404:
        assert response.json()["detail"] == "Shift not found"