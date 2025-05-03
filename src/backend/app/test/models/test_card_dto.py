import pytest
from backend.app.models.card import CardCreate, CardOut

def test_card_create_to_dict():
    card = CardCreate(id=1, tipo="credito", balance=100.5)
    result = card.to_dict()
    assert result == {"id": 1, "tipo": "credito", "balance": 100.5}

def test_card_create_get_fields():
    fields = CardCreate.get_fields()
    expected_fields = {
        "id": "INTEGER PRIMARY KEY",
        "tipo": "TEXT",
        "balance": "REAL"
    }
    assert fields == expected_fields

def test_card_out_from_dict():
    data = {"id": 2, "tipo": "debito", "balance": 250.75}
    card = CardOut.from_dict(data)
    assert isinstance(card, CardOut)
    assert card.id == 2
    assert card.tipo == "debito"
    assert card.balance == 250.75
