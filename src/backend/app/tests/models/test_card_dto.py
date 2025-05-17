import pytest
from backend.app.models.card import CardCreate, CardOut

# Prueba: Crear una tarjeta correctamente
def test_card_create():
    card = CardCreate(ID=1, IDUsuario=101, IDTipoTarjeta=1, Saldo=1000)
    assert card.ID == 1
    assert card.IDUsuario == 101
    assert card.IDTipoTarjeta == 1
    assert card.Saldo == 1000

# Prueba: Crear una tarjeta con valores por defecto
def test_card_create_with_defaults():
    card = CardCreate()
    assert card.ID is None
    assert card.IDUsuario is None
    assert card.IDTipoTarjeta is None
    assert card.Saldo is None

# Prueba: Verificar el método to_dict
def test_card_to_dict():
    card = CardCreate(ID=2, IDUsuario=202, IDTipoTarjeta=2, Saldo=500)
    card_dict = card.to_dict()
    assert isinstance(card_dict, dict)
    assert card_dict == {
        "ID": 2,
        "IDUsuario": 202,
        "IDTipoTarjeta": 2,
        "Saldo": 500
    }

# Prueba: Obtener campos del modelo
def test_card_get_fields():
    expected_fields = {
        "ID": "INTEGER PRIMARY KEY",
        "IDUsuario": "INTEGER",
        "IDTipoTarjeta": "INTEGER",
        "Saldo": "INTEGER"
    }
    assert CardCreate.get_fields() == expected_fields

# Prueba: Crear una tarjeta de salida a partir de un diccionario
def test_card_out_from_dict():
    data = {
        "ID": 3,
        "IDUsuario": 303,
        "IDTipoTarjeta": 3,
        "Saldo": 750
    }
    card_out = CardOut.from_dict(data)
    assert isinstance(card_out, CardOut)
    assert card_out.ID == 3
    assert card_out.IDUsuario == 303
    assert card_out.IDTipoTarjeta == 3
    assert card_out.Saldo == 750

# Prueba: Verificar que el método from_dict falle con datos inválidos
def test_card_out_from_dict_invalid():
    with pytest.raises(TypeError):
        CardOut.from_dict("invalid data")

# Prueba: Verificar el nombre de la entidad en CardCreate
def test_card_create_entity_name():
    assert CardCreate.__entity_name__ == "TarjetaIns"

# Prueba: Verificar el nombre de la entidad en CardOut
def test_card_out_entity_name():
    assert CardOut.__entity_name__ == "TarjetaIns"
