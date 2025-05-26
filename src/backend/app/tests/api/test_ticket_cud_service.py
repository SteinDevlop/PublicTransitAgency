import pytest
import logging
from fastapi.testclient import TestClient
from backend.app.api.routes.ticket_cud_service import app as tickets_router
from backend.app.logic.universal_controller_instance import universal_controller as controller

from backend.app.models.ticket import Ticket
from backend.app.core.conf import headers
from fastapi import FastAPI

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("backend.app.api.routes.ticket_cud_service")

app_for_test = FastAPI()
app_for_test.include_router(tickets_router)
client = TestClient(app_for_test, raise_server_exceptions=False)

def test_crear_ticket():
    ticket_id = 9999
    try:
        response = client.post("/tickets/create", data={
            "ID": ticket_id,
            "EstadoIncidencia": "Abierto"
        }, headers=headers)
        assert response.status_code == 200
        assert response.json()["message"] == "Ticket creado exitosamente."
        ticket = controller.get_by_id(Ticket, ticket_id)
        assert ticket is not None
        assert ticket.EstadoIncidencia == "Abierto"
        logger.info("Test crear_ticket ejecutado correctamente.")
    finally:
        ticket = controller.get_by_id(Ticket, ticket_id)
        if ticket:
            controller.delete(ticket)

def test_actualizar_ticket():
    ticket_id = 9999
    try:
        ticket = Ticket(ID=ticket_id, EstadoIncidencia="Abierto")
        controller.add(ticket)
        response = client.post("/tickets/update", data={
            "ID": ticket_id,
            "EstadoIncidencia": "Cerrado"
        }, headers=headers)
        assert response.status_code == 200
        assert response.json()["message"] == "Ticket actualizado exitosamente."
        ticket_actualizado = controller.get_by_id(Ticket, ticket_id)
        assert ticket_actualizado is not None
        assert ticket_actualizado.EstadoIncidencia == "Cerrado"
        logger.info(f"Test actualizar_ticket ejecutado correctamente para ID={ticket_id}.")
    finally:
        ticket = controller.get_by_id(Ticket, ticket_id)
        if ticket:
            controller.delete(ticket)

def test_eliminar_ticket():
    ticket_id = 99999
    ticket = Ticket(ID=ticket_id, EstadoIncidencia="Abierto")
    controller.add(ticket)
    response = client.post("/tickets/delete", data={"ID": ticket_id}, headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Ticket eliminado exitosamente."
    ticket_eliminado = controller.get_by_id(Ticket, ticket_id)
    assert ticket_eliminado is None
    logger.info(f"Test eliminar_ticket ejecutado correctamente para ID={ticket_id}.")

def test_eliminar_ticket_no_existente():
    ticket_id = 999999
    response = client.post("/tickets/delete", data={"ID": ticket_id}, headers=headers)
    assert response.status_code in (404, 500)
    logger.warning(
        f"Test eliminar_ticket_no_existente ejecutado: status={response.status_code}, body={response.text}"
    )