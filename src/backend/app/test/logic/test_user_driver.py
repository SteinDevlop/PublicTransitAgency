# tests/test_worker.py

import pytest
from unittest.mock import MagicMock
from backend.app.logic.user_driver import Worker

@pytest.fixture
def mock_card():
    return MagicMock()  # simulamos el CardOperative

def test_worker_creation_valid(mock_card):
    worker = Worker(
        id_user=1,
        type_identification="DNI",
        identification=12345678,
        name="John Doe",
        email="john.doe@example.com",
        password="Secure@Pass123",
        role="Driver",
        card=mock_card
    )
    assert worker.id_user == 1
    assert worker.name == "John Doe"
    assert worker.routes_assigmented == []

def test_worker_invalid_name(mock_card):
    with pytest.raises(ValueError, match="Invalid Name"):
        Worker(
            id_user=2,
            type_identification="DNI",
            identification=87654321,
            name="",
            email="john.doe@example.com",
            password="Secure@Pass123",
            role="Driver",
            card=mock_card
        )

def test_worker_invalid_email(mock_card):
    with pytest.raises(ValueError, match="Invalid Email"):
        Worker(
            id_user=3,
            type_identification="DNI",
            identification=12345678,
            name="Jane Doe",
            email="invalid-email",
            password="Secure@Pass123",
            role="Driver",
            card=mock_card
        )

def test_worker_invalid_password(mock_card):
    with pytest.raises(ValueError, match="Invalid Password"):
        Worker(
            id_user=4,
            type_identification="DNI",
            identification=12345678,
            name="Jane Doe",
            email="jane.doe@example.com",
            password="123",
            role="Driver",
            card=mock_card
        )

def test_get_driver_assignment():
    driver = Worker(
        id_user=5,
        type_identification="DNI",
        identification=12345678,
        name="Driver One",
        email="driver.one@example.com",
        password="Driver@Pass123",
        role="Driver",
        card=mock_card
    )
    # Simulamos que el driver tiene rutas asignadas
    driver.routes_assigmented = ["Route 1", "Route 2"]

    assert driver.get_driver_assigment() == ["Route 1", "Route 2"]
