from fastapi.testclient import TestClient
from backend.app.api.routes.ticket_query_service import app as tickets_router
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

def test_listar_tickets():
    controller.add(Ticket(ID=1, EstadoIncidencia="Abierto"))
    response = client.get("/tickets/")
    assert response.status_code == 200
    assert "Abierto" in response.text

def test_detalle_ticket_existente():
    controller.add(Ticket(ID=1, EstadoIncidencia="Abierto"))
    response = client.get("/tickets/1")
    assert response.status_code == 200
    assert "Abierto" in response.text

def test_detalle_ticket_no_existente():
    response = client.get("/tickets/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Ticket no encontrado"