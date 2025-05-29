import pytest
from backend.app.logic.card_user import CardUser

def test_use_card_sufficient_balance():
    card = CardUser(id_card=1, card_type="Pasajero", balance=5000, user_id=100)
    result = card.use_card()
    assert result is True
    assert card.balance == 2000

def test_use_card_insufficient_balance():
    card = CardUser(id_card=2, card_type="Pasajero", balance=2000, user_id=101)
    result = card.use_card()
    assert result is False
    assert card.balance == 2000
