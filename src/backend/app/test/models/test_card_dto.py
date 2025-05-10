import pytest
from backend.app.models.card import CardCreate, CardOut

# Prueba: Crear una tarjeta correctamente
def test_card_create():
    card = CardCreate(id=1, iduser=101, idtype=1, balance=1000)
    assert card.id == 1
    assert card.iduser == 101
    assert card.idtype == 1
    assert card.balance == 1000

# Prueba: Crear una tarjeta con valores por defecto
def test_card_create_with_defaults():
    card = CardCreate()
    assert card.id is None
    assert card.iduser is None
    assert card.idtype is None
    assert card.balance is None

# Prueba: Verificar el método to_dict
def test_card_to_dict():
    card = CardCreate(id=2, iduser=202, idtype=2, balance=500)
    card_dict = card.to_dict()
    assert isinstance(card_dict, dict)
    assert card_dict == {
        "id": 2,
        "iduser": 202,
        "idtype": 2,
        "balance": 500
    }

# Prueba: Obtener campos del modelo
def test_card_get_fields():
    expected_fields = {
        "id": "INTEGER PRIMARY KEY",
        "iduser": "INTEGER",
        "idtype": "INTEGER",
        "balance": "INTEGER"
    }
    assert CardCreate.get_fields() == expected_fields

# Prueba: Crear una tarjeta de salida a partir de un diccionario
def test_card_out_from_dict():
    data = {
        "id": 3,
        "iduser": 303,
        "idtype": 3,
        "balance": 750
    }
    card_out = CardOut.from_dict(data)
    assert isinstance(card_out, CardOut)
    assert card_out.id == 3
    assert card_out.iduser == 303
    assert card_out.idtype == 3
    assert card_out.balance == 750

# Prueba: Verificar que el método from_dict falle con datos inválidos
def test_card_out_from_dict_invalid():
    with pytest.raises(TypeError):
        CardOut.from_dict("invalid data")

# Prueba: Verificar el nombre de la entidad en CardCreate
def test_card_create_entity_name():
    assert CardCreate.__entity_name__ == "tarjeta"

# Prueba: Verificar el nombre de la entidad en CardOut
def test_card_out_entity_name():
    assert CardOut.__entity_name__ == "tarjeta"
