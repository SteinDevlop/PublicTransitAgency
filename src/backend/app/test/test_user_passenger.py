# test_passenger.py

import pytest
from unittest.mock import MagicMock, patch
from src.backend.app.logic.user_passenger import Passenger
from src.backend.app.logic.card_user import CardUser

# Datos simulados
mock_card = MagicMock(spec=CardUser)
mock_card.id_card = 1
mock_card.balance = 100.0
mock_card.balance.return_value = {"balance": 100.0}
mock_card.recharge.return_value = True
mock_card.pay.return_value = True
mock_card.get_card_information.return_value = {"balance": 100.0}
mock_card.use_card.return_value = True


def test_passenger_creation_valid():
    passenger = Passenger(
        id_user=1,
        type_identification="ID",
        identification=123456,
        name="John Doe",
        email="john@example.com",
        password="Strong@Password123",
        role="passenger",
        card=mock_card
    )
    assert passenger.name == "John Doe"
    assert passenger.email == "john@example.com"

def test_passenger_invalid_name():
    with pytest.raises(ValueError, match="Invalid Name"):
        Passenger(
            id_user=1,
            type_identification="ID",
            identification=123456,
            name="",  # Nombre inválido
            email="john@example.com",
            password="Strong@Password123",
            role="passenger",
            card=mock_card
        )

def test_passenger_invalid_email():
    with pytest.raises(ValueError, match="Invalid Email"):
        Passenger(
            id_user=1,
            type_identification="ID",
            identification=123456,
            name="John Doe",
            email="invalid-email",
            password="Strong@Password123",
            role="passenger",
            card=mock_card
        )

def test_passenger_invalid_password():
    with pytest.raises(ValueError, match="Invalid Password"):
        Passenger(
            id_user=1,
            type_identification="ID",
            identification=123456,
            name="John Doe",
            email="john@example.com",
            password="123",  # Contraseña débil
            role="passenger",
            card=mock_card
        )

def test_get_route_information_success():
    passenger = Passenger(
        id_user=1,
        type_identification="ID",
        identification=123456,
        name="John Doe",
        email="john@example.com",
        password="Strong@Password123",
        role="passenger",
        card=mock_card
    )
    with patch('src.backend.app.logic.routes.Routes.get_route_id', return_value="route_data") as mock_get_route:
        route_info = passenger.get_route_information("route123")
        assert route_info == "route_data"
        mock_get_route.assert_called_once_with("route123")


def test_get_stop_information_success():
    passenger = Passenger(
        id_user=1,
        type_identification="ID",
        identification=123456,
        name="John Doe",
        email="john@example.com",
        password="Strong@Password123",
        role="passenger",
        card=mock_card
    )
    with patch('src.backend.app.logic.stops.Stops.get_stop_id', return_value="stop_data") as mock_get_stop:
        stop_info = passenger.get_stop_information("stop123")
        assert stop_info == "stop_data"
        mock_get_stop.assert_called_once_with("stop123")


def test_get_card_information_success():
    passenger = Passenger(
        id_user=1,
        type_identification="ID",
        identification=123456,
        name="John Doe",
        email="john@example.com",
        password="Strong@Password123",
        role="passenger",
        card=mock_card
    )
    card_info = passenger.card.get_card_information(card_id=mock_card.id_card)
    assert card_info == {"balance": 100.0}

def test_use_card_pay(monkeypatch):
    passenger = Passenger(
        id_user=1,
        type_identification="ID",
        identification=123456,
        name="John Doe",
        email="john@example.com",
        password="Strong@Password123",
        role="passenger",
        card=mock_card
    )

    inputs = iter(["100", "card"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    # Parchear los métodos internos pay, recharge, get_card_information
    with patch.object(passenger, "pay") as mock_pay:
        passenger.use_card("pay")
        mock_pay.assert_called_once_with("100", "card")  # input dos veces el mismo valor

def test_use_card_recharge(monkeypatch):
    passenger = Passenger(
        id_user=1,
        type_identification="ID",
        identification=123456,
        name="John Doe",
        email="john@example.com",
        password="Strong@Password123",
        role="passenger",
        card=mock_card
    )

    inputs = iter(["100", "card"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    with patch.object(passenger, "recharge") as mock_recharge:
        passenger.use_card("recharge")
        mock_recharge.assert_called_once_with("100", "card")

def test_use_card_get_card_information():
    passenger = Passenger(
        id_user=1,
        type_identification="ID",
        identification=123456,
        name="John Doe",
        email="john@example.com",
        password="Strong@Password123",
        role="passenger",
        card=mock_card
    )

    with patch.object(passenger, "get_card_information") as mock_get_info:
        passenger.use_card("get_card_information")
        mock_get_info.assert_called_once()

def test_plan_route(monkeypatch):
    passenger = Passenger(
        id_user=1,
        type_identification="ID",
        identification=123456,
        name="John Doe",
        email="john@example.com",
        password="Strong@Password123",
        role="passenger",
        card=mock_card
    )

    # Simular inputs de origen y destino
    inputs = iter(["OriginParade", "DestinationParade"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    with patch('src.backend.app.logic.routes.Routes') as mock_routes_class:
        mock_route_instance = mock_routes_class.return_value
        route = passenger.plan_route()
        assert route == mock_route_instance

def test_use_card_invalid_operation():
    passenger = Passenger(
        id_user=1,
        type_identification="ID",
        identification=123456,
        name="John Doe",
        email="john@example.com",
        password="Strong@Password123",
        role="passenger",
        card=mock_card
    )
    
    with pytest.raises(ValueError, match="Invalid operation"):
        passenger.use_card("invalid_operation")
