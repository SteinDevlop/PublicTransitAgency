import pytest
from fastapi.testclient import TestClient
from backend.app.api.routes.ticket_query_service import app as tickets_router
from backend.app.logic.universal_controller_sql import UniversalController
from backend.app.models.ticket import Ticket
from backend.app.core.conf import headers  # Import headers for authentication
from fastapi import FastAPI
from unittest.mock import patch

app_for_test = FastAPI()
app_for_test.include_router(tickets_router)
client = TestClient(app_for_test)
controller = UniversalController()

@pytest.fixture(autouse=True)
def mock_get_current_user():
    with patch("backend.app.core.auth.get_current_user") as mock_user:
        mock_user.return_value = {"user_id": 1, "scopes": ["system", "administrador", "supervisor"]}
        yield mock_user

def setup_function():
    controller.clear_tables()

def teardown_function():
    controller.clear_tables()

def test_listar_tickets():
    controller.add(Ticket(ticket_id=1, status_code=1))
    response = client.get("/tickets/", headers=headers)
    assert response.status_code == 200
    assert "1" in response.text

def test_detalle_ticket_existente():
    controller.add(Ticket(ticket_id=1, status_code=1))
    response = client.get("/tickets/1", headers=headers)
    assert response.status_code == 200
    assert "1" in response.text

def test_detalle_ticket_no_existente():
    response = client.get("/tickets/999", headers=headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "Ticket no encontrado"