import pytest
from backend.app.models.type_card import TypeCardCreate, TypeCardOut

def test_type_card_create_to_dict():
    tc = TypeCardCreate(id=1, type="Visa")
    assert tc.to_dict() == {"id": 1, "type": "Visa"}

def test_type_card_get_fields():
    expected = {
        "id": "INTEGER PRIMARY KEY",
        "type": "TEXT"
    }
    assert TypeCardCreate.get_fields() == expected

def test_type_card_out_from_dict():
    data = {"id": 2, "type": "MasterCard"}
    tc = TypeCardOut.from_dict(data)
    assert isinstance(tc, TypeCardOut)
    assert tc.id == 2
    assert tc.type == "MasterCard"