import pytest
from backend.app.logic.user_administrator import Administrator
from backend.app.logic.card_operative import CardOperative
from backend.app.logic.routes import Routes
from backend.app.logic.stops import Stops
from backend.app.logic.unit_transport import Transport
from backend.app.logic.user_driver import Worker
from backend.app.logic.ticket import Ticket
from unittest.mock import MagicMock

@pytest.fixture
def mock_card():
    return MagicMock()

@pytest.fixture
def mock_ticket():
    return MagicMock()

@pytest.fixture
def admin(mock_card):
    return Administrator(
        id_user=1,
        type_identification="CC",
        identification=123456789,
        name="Admin User",
        email="admin@example.com",
        password="Secure@Pass123",
        role="Administrator",
        card=mock_card  # <- sin paréntesis
    )

@pytest.fixture
def sample_driver(mock_card):
    return Worker(
        id_user=2,
        type_identification="CC",
        identification=987654321,
        name="Driver User",
        email="driver@example.com",
        password="Driver@Pass456",
        role="Driver",
        card=mock_card  # <- sin paréntesis
    )

@pytest.fixture
def sample_route():
    route_info = {"route_id": "R001", "stops": ["Stop1", "Stop2"], "schedule": "8:00-18:00"}
    return Routes(route_info)

@pytest.fixture
def sample_stop():
    stop_info = {"stop_id": "S001", "name": "Central Station", "location": "Downtown"}
    return Stops(stop_info)

@pytest.fixture
def sample_ticket(mock_ticket):
    return mock_ticket  # <- sin paréntesis

# Aquí ya van los tests
def test_assign_route(admin, sample_driver, sample_route):
    admin.assign_route(sample_driver, sample_route)
    assert sample_route in sample_driver.routes_assigmented

def test_create_parade(admin):
    parade_info = {"stop_id": "S002", "name": "North Park", "location": "Uptown"}
    parade = admin.create_parade(parade_info)
    assert isinstance(parade, Stops)
    assert parade._stop["name"] == "North Park"

def test_create_route(admin):
    route_info = {"route_id": "R002", "stops": ["S001", "S002"], "schedule": "9:00-17:00"}
    route = admin.create_route(route_info)
    assert isinstance(route, Routes)
    assert route._route["schedule"] == "9:00-17:00"

def test_create_vehicle(admin, sample_ticket):
    vehicle = admin.create_vehicle("V001", "Bus", sample_ticket, "Garage 1", 50)
    assert isinstance(vehicle, Transport)
    assert vehicle._capacity == 50

def test_set_get_user_information(admin, sample_driver):
    admin.get_user_information(sample_driver)
    admin.set_user_information(sample_driver, "name", "New Driver Name")
    assert sample_driver.name == "New Driver Name"
