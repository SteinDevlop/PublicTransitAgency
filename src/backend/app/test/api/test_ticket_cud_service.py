import pytest
from fastapi.testclient import TestClient
from backend.app.api.routes.ticket_cud_service import app as tickets_router
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

def test_crear_ticket():
    response = client.post("/tickets/create", data={
        "id": 1,
        "estadoincidencia": "Abierto"
    }, headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Ticket creado exitosamente."

def test_actualizar_ticket():
    controller.add(Ticket(id=1, estadoincidencia="Abierto"))
    response = client.post("/tickets/update", data={
        "id": 1,
        "estadoincidencia": "Cerrado"
    }, headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Ticket actualizado exitosamente."

def test_eliminar_ticket():
    controller.add(Ticket(id=1, estadoincidencia="Abierto"))
    response = client.post("/tickets/delete", data={"id": 1}, headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Ticket eliminado exitosamente."