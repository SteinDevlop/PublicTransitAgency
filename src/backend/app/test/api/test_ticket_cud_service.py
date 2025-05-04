import pytest
from fastapi.testclient import TestClient
from backend.app.api.routes.ticket_CUD_service import app as tickets_router
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

def test_crear_ticket():
    response = client.post("/tickets/create", data={
        "ticket_id": 1,
        "status_code": 1
    }, headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Ticket creado exitosamente."

def test_actualizar_ticket():
    controller.add(Ticket(ticket_id=1, status_code=1))
    response = client.post("/tickets/update", data={
        "ticket_id": 1,
        "status_code": 2
    }, headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Ticket actualizado exitosamente."

def test_eliminar_ticket():
    controller.add(Ticket(ticket_id=1, status_code=1))
    response = client.post("/tickets/delete", data={"ticket_id": 1}, headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Ticket eliminado exitosamente."