import pytest
from fastapi.testclient import TestClient
from backend.app.api.routes.ticket_query_service import app as ticket_router
from backend.app.models.ticket import TicketCreate
#from backend.app.api.routes.ticket_cud_service import app as ticket_router
from backend.app.logic.universal_controller_sql import UniversalController

client = TestClient(ticket_router)

def setup_function():
    UniversalController().clear_tables()

def test_crear_ticket():
    response = client.post("/ticket/create", data={"ticket_id": 1, "status_code": 1})
    assert response.status_code == 303

def test_actualizar_ticket():
    controller = UniversalController()
    controller.add(TicketCreate(ticket_id=1, status_code=1))
    response = client.post("/ticket/update", data={"ticket_id": 1, "status_code": 2})
    assert response.status_code == 303

def test_eliminar_ticket():
    controller = UniversalController()
    controller.add(TicketCreate(ticket_id=1, status_code=1))
    response = client.post("/ticket/delete", data={"ticket_id": 1})
    assert response.status_code == 303