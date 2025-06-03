import pytest
import logging
from fastapi.testclient import TestClient
from backend.app.api.routes.ticket_query_service import app as tickets_router
from backend.app.logic.universal_controller_instance import universal_controller as controller

from backend.app.models.ticket import Ticket
from backend.app.core.conf import headers
from fastapi import FastAPI

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("backend.app.api.routes.ticket_query_service")

app_for_test = FastAPI()
app_for_test.include_router(tickets_router)
client = TestClient(app_for_test, raise_server_exceptions=False)

def test_listar_tickets():
    ticket_id = 9999
    try:
        ticket = Ticket(ID=ticket_id, EstadoIncidencia="Abierto Test")
        controller.add(ticket)
        response = client.get("/tickets/", headers=headers)
        assert response.status_code == 200
        tickets = response.json()
        assert isinstance(tickets, list)
        assert any(t.get("ID") == ticket_id for t in tickets)
        logger.info("Test listar_tickets ejecutado correctamente.")
    finally:
        ticket = controller.get_by_id(Ticket, ticket_id)
        if ticket:
            controller.delete(ticket)


def test_detalle_ticket_existente():
    ticket_id = 9999
    try:
        ticket = Ticket(ID=ticket_id, EstadoIncidencia="Abierto Test")
        controller.add(ticket)
        response = client.get(f"/tickets/{ticket_id}", headers=headers)
        assert response.status_code == 200
        assert "Abierto Test" in response.text or str(ticket_id) in response.text
        logger.info(f"Test detalle_ticket_existente ejecutado correctamente para ID={ticket_id}.")
    finally:
        ticket = controller.get_by_id(Ticket, ticket_id)
        if ticket:
            controller.delete(ticket)

def test_listar_tickets_sin_datos():
    ticket_id = 9999
    try:
        ticket = controller.get_by_id(Ticket, ticket_id)
        if ticket:
            controller.delete(ticket)
        response = client.get("/tickets/", headers=headers)
        assert response.status_code == 200
        assert "Abierto Test" not in response.text and str(ticket_id) not in response.text
        logger.info("Test listar_tickets_sin_datos ejecutado correctamente.")
    finally:
        ticket = controller.get_by_id(Ticket, ticket_id)
        if ticket:
            controller.delete(ticket)

def test_detalle_ticket_no_existente():
    ticket_id = 99999
    response = client.get(f"/tickets/{ticket_id}", headers=headers)
    assert response.status_code in (404, 500)
    logger.warning(
        f"Test detalle_ticket_no_existente ejecutado: status={response.status_code}, body={response.text}"
    )