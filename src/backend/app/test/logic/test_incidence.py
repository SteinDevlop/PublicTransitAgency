import pytest
from backend.app.logic.incidence import Incidence
from backend.app.logic.ticket import Ticket

def test_incidence_initialization():
    ticket = Ticket(id=1, description="Test Ticket")  # Simula un objeto Ticket
    incidence = Incidence(description="Test Incidence", status=ticket, type="Technical", incidence_id=1)

    assert incidence.description == "Test Incidence"
    assert incidence.status == ticket
    assert incidence.type == "Technical"
    assert incidence.incidence_id == 1

def test_incidence_setters():
    ticket = Ticket(id=1, description="Test Ticket")  # Simula un objeto Ticket
    new_ticket = Ticket(id=2, description="Updated Ticket")
    incidence = Incidence(description="Test Incidence", status=ticket, type="Technical", incidence_id=1)

    incidence.description = "Updated Incidence"
    incidence.status = new_ticket
    incidence.type = "Operational"
    incidence.incidence_id = 2

    assert incidence.description == "Updated Incidence"
    assert incidence.status == new_ticket
    assert incidence.type == "Operational"
    assert incidence.incidence_id == 2

def test_update_incidence():
    ticket = Ticket(id=1, description="Test Ticket")  # Simula un objeto Ticket
    new_ticket = Ticket(id=2, description="Updated Ticket")
    incidence = Incidence(description="Test Incidence", status=ticket, type="Technical", incidence_id=1)

    incidence.update_incidence(description="Updated Incidence", status=new_ticket, type="Operational", incidence_id=2)

    assert incidence.description == "Updated Incidence"
    assert incidence.status == new_ticket
    assert incidence.type == "Operational"
    assert incidence.incidence_id == 2

def test_update_incidence_without_id():
    ticket = Ticket(id=1, description="Test Ticket")  # Simula un objeto Ticket
    incidence = Incidence(description="Test Incidence", status=ticket, type="Technical", incidence_id=1)

    with pytest.raises(ValueError, match="Incidence ID is required."):
        incidence.update_incidence(description="Updated Incidence", status=ticket, type="Operational", incidence_id=None)