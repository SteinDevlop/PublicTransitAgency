from fastapi.testclient import TestClient
from backend.app.api.routes.ticket_CUD_service import app as tickets_router
from backend.app.logic.universal_controller_sql import UniversalController
from backend.app.models.ticket import Ticket
from fastapi import FastAPI

app_for_test = FastAPI()
app_for_test.include_router(tickets_router)
client = TestClient(app_for_test)
controller = UniversalController()

def setup_function():
    controller.clear_tables()

def teardown_function():
    controller.clear_tables()

def test_crear_ticket():
    response = client.post("/tickets/create", data={"ticket_id": 1, "status_code": 1})
    assert response.status_code == 200

def test_actualizar_ticket():
    controller.add(Ticket(ticket_id=1, status_code=1))
    response = client.post("/tickets/update", data={"ticket_id": 1, "status_code": 2})
    assert response.status_code == 200

def test_eliminar_ticket():
    controller.add(Ticket(ticket_id=1, status_code=1))
    response = client.post("/tickets/delete", data={"ticket_id": 1})
    assert response.status_code == 200