import pytest
from unittest.mock import MagicMock, patch
from backend.app.logic.user_passenger import Passenger
from backend.app.logic.card_user import CardUser
from backend.app.logic.payments import Payments
from backend.app.logic.routes import Routes
from backend.app.logic.stops import Stops


# Datos simulados
mock_card = MagicMock(spec=CardUser)
mock_card.id_card = 1
mock_card.balance = 100.0
mock_card.get_card_information.return_value = {"balance": 100.0}
"""mock_route = MagicMock(spec=Routes)
mock_route.get_route_information.return_value = "route_data"
mock_stop = MagicMock(spec=Stops)
mock_stop.get_stop_information.return_value = "stop_data"
mock_payments = MagicMock(spec=Payments)
mock_payments.process_payment.return_value = True"""

@pytest.fixture
def passenger():
    return Passenger(
        id_user=1,
        type_identification="ID",
        identification=123456,
        name="John Doe",
        email="john@example.com",
        password="Strong@Password123",
        role="passenger",
        card=mock_card
    )


def test_passenger_creation_valid(passenger):
    assert passenger.name == "John Doe"
    assert passenger.email == "john@example.com"


def test_use_card_pay(passenger, monkeypatch):
    # Simulamos inputs del usuario
    inputs = iter(["100", "card"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    with patch.object(passenger, "_pay") as mock_pay:
        passenger.use_card("pay")
        mock_pay.assert_called_once()


def test_use_card_recharge(passenger, monkeypatch):
    # Simulamos inputs del usuario
    inputs = iter(["100", "card"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    with patch.object(passenger, "_recharge") as mock_recharge:
        passenger.use_card("recharge")
        mock_recharge.assert_called_once()


def test_get_card_information(passenger):
    card_info = passenger.use_card("get_card_information")
    assert card_info == {"balance": 100.0}
    mock_card.get_card_information.assert_called_once()


def test_use_card_invalid_operation(passenger):
    with pytest.raises(ValueError, match="Invalid operation"):
        passenger.use_card("invalid_operation")


"""def test_get_route_information(passenger):
    with patch.object(Routes, 'get_route_information', return_value="route_data") as mock_route_info:
        route_info = passenger.get_route_information("route123")
        assert route_info == "route_data"
        mock_route_info.assert_called_once_with("route123")"""


"""def test_get_route_information_not_found(passenger):
    with patch.object(Routes, 'get_route_information', return_value=None) as mock_route_info:
        with pytest.raises(ValueError, match="Route not found"):
            passenger.get_route_information("route123")"""


"""def test_get_stop_information(passenger):
    with patch.object(Stops, 'get_stop_information', return_value="stop_data") as mock_stop_info:
        stop_info = passenger.get_stop_information("stop123")
        assert stop_info == "stop_data"
        mock_stop_info.assert_called_once_with("stop123")"""


"""def test_get_stop_information_not_found(passenger):
    with patch.object(Stops, 'get_stop_information', return_value=None) as mock_stop_info:
        with pytest.raises(ValueError, match="Stop not found"):
            passenger.get_stop_information("stop123")"""


"""def test_plan_route(passenger, monkeypatch):
    inputs = iter(["OriginParade", "DestinationParade"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    with patch.object(Routes, 'plan_route', return_value="route_data") as mock_plan_route:
        route = passenger.plan_route()
        assert route == "route_data"
        mock_plan_route.assert_called_once_with("OriginParade", "DestinationParade")"""


"""def test_plan_route_not_found(passenger, monkeypatch):
    inputs = iter(["OriginParade", "DestinationParade"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    with patch.object(Routes, 'plan_route', return_value=None) as mock_plan_route:
        with pytest.raises(ValueError, match="Route not found"):
            passenger.plan_route()"""
