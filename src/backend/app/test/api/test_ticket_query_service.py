import pytest
from fastapi.testclient import TestClient
from backend.app.api.routes.ticket_query_service import app as ticket_router
from backend.app.logic.universal_controller_sql import UniversalController
from backend.app.models.ticket import TicketCreate

client = TestClient(ticket_router)

def setup_function():
    UniversalController().clear_tables()

def test_listar_tickets():
    response = client.get("/tickets/")
    assert response.status_code == 200

def test_detalle_ticket_existente():
    controller = UniversalController()
    controller.add(TicketCreate(ticket_id=1, status_code=1))
    response = client.get("/tickets/1")
    assert response.status_code == 200

def test_detalle_ticket_no_existente():
    response = client.get("/tickets/999")
    assert response.status_code == 404