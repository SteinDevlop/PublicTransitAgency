"""import pytest
from fastapi.testclient import TestClient
from backend.app.api.routes.ticket_cud_service import app  

client = TestClient(app)

@pytest.fixture
def setup_ticket():
    return {"ticket_id": "123", "status_code": 1}

def test_create_ticket(setup_ticket):
    response = client.post(
        "/ticket/create",
        data={
            "status_code": setup_ticket["status_code"],
            "ticket_id": setup_ticket["ticket_id"]
        }
    )
    assert response.status_code == 200
    assert response.json()["operation"] == "create"
    assert response.json()["message"] == f"Ticket {setup_ticket['ticket_id']} creado"

def test_create_ticket_invalid_status():
    response = client.post(
        "/ticket/create",
        data={
            "status_code": 4,  
            "ticket_id": "124"
        }
    )
    assert response.status_code == 400
    assert "Código de estado debe ser 1, 2 o 3" in response.json()["detail"]

def test_update_ticket(setup_ticket):
    response = client.post(
        "/ticket/update",
        data={
            "ticket_id": setup_ticket["ticket_id"],
            "status_code": 2  
        }
    )
    assert response.status_code == 200
    assert response.json()["operation"] == "update"
    assert response.json()["message"] == f"Ticket {setup_ticket['ticket_id']} actualizado"

def test_update_ticket_not_found():
    response = client.post(
        "/ticket/update",
        data={
            "ticket_id": "999",  
            "status_code": 2
        }
    )
    assert response.status_code == 404
    assert "Ticket no encontrado" in response.json()["detail"]

def test_delete_ticket(setup_ticket):
    response = client.post(
        "/ticket/delete",
        data={"ticket_id": setup_ticket["ticket_id"]}
    )
    assert response.status_code == 200
    assert response.json()["operation"] == "delete"
    assert response.json()["message"] == f"Ticket {setup_ticket['ticket_id']} eliminado"

def test_delete_ticket_not_found():
    response = client.post(
        "/ticket/delete",
        data={"ticket_id": "999"} 
    )
    assert response.status_code == 404
    assert "Ticket no encontrado" in response.json()["detail"]
"""