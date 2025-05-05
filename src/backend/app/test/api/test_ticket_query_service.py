import pytest
from fastapi.testclient import TestClient
from backend.app.api.routes.ticket_query_service import app as tickets_router
from backend.app.logic.universal_controller_postgres import UniversalController
from backend.app.models.ticket import Ticket
from backend.app.core.conf import headers
from fastapi import FastAPI

app_for_test = FastAPI()
app_for_test.include_router(tickets_router)
client = TestClient(app_for_test)
controller = UniversalController()

@pytest.fixture(autouse=True)
def setup_and_teardown():
    controller.clear_tables()
    yield
    controller.clear_tables()

def test_listar_tickets():
    controller.add(Ticket(id=999, estadoincidencia="Abierto"))
    response = client.get("/tickets/", headers=headers)
    assert response.status_code == 200
    assert "Abierto" in response.text

def test_detalle_ticket_existente():
    controller.add(Ticket(id=999, estadoincidencia="Abierto"))
    response = client.get("/tickets/999", headers=headers)
    assert response.status_code == 200
    assert "Abierto" in response.text


def test_detalle_ticket_no_existente():
    response = client.get("/tickets/998", headers=headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "Ticket no encontrado"
