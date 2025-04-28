import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from backend.app.services.movement_service import app  # Ajusta si el módulo tiene otro nombre
from backend.app.models.movement import MovementOut

# Montamos la app de test
client = TestClient(app)

# Mock data de prueba
movement_example = MovementOut(id=1, type="Ingreso", amount=1000.0)

# Test para consultar la página HTML
def test_consultar_page():
    response = client.get("/consultar")
    assert response.status_code == 200
    assert "html" in response.headers["content-type"]

# Test para obtener todos los movimientos
@patch("backend.app.services.movement_service.controller.read_all")
def test_get_movimientos(mock_read_all):
    mock_read_all.return_value = [movement_example]
    
    response = client.get("/movimientos")
    assert response.status_code == 200
    assert response.json() == [movement_example.dict()]

# Test para ver un movimiento por id - cuando existe
@patch("backend.app.services.movement_service.controller.get_by_id")
def test_movimiento_found(mock_get_by_id):
    mock_get_by_id.return_value = movement_example

    response = client.get("/movimiento?id=1")
    assert response.status_code == 200
    assert "Ingreso" in response.text
    assert "1000.0" in response.text

# Test para ver un movimiento por id - cuando NO existe
@patch("backend.app.services.movement_service.controller.get_by_id")
def test_movimiento_not_found(mock_get_by_id):
    mock_get_by_id.return_value = None

    response = client.get("/movimiento?id=999")
    assert response.status_code == 200
    assert "None" in response.text
