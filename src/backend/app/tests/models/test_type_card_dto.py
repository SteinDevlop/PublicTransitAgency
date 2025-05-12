import pytest
from backend.app.models.type_card import TypeCardCreate, TypeCardOut

# Prueba: Crear un tipo de tarjeta correctamente
def test_type_card_create():
    type_card = TypeCardCreate(id=1, type="VIP")

    assert type_card.id == 1
    assert type_card.type == "VIP"

# Prueba: Crear un tipo de tarjeta con valores por defecto
def test_type_card_create_defaults():
    type_card = TypeCardCreate()

    assert type_card.id is None
    assert type_card.type is None

# Prueba: Conversión a diccionario con to_dict
def test_type_card_to_dict():
    type_card = TypeCardCreate(id=2, type="Regular")
    type_card_dict = type_card.to_dict()

    assert isinstance(type_card_dict, dict)
    assert type_card_dict == {
        "id": 2,
        "type": "Regular"
    }

# Prueba: Obtener campos del modelo
def test_type_card_get_fields():
    expected_fields = {
        "id": "INTEGER PRIMARY KEY",
        "type": "VARCHAR(20)"
    }
    assert TypeCardCreate.get_fields() == expected_fields

# Prueba: Crear una instancia de TypeCardOut desde un diccionario
def test_type_card_out_from_dict():
    data = {
        "id": 3,
        "type": "Student"
    }
    type_card_out = TypeCardOut.from_dict(data)

    assert isinstance(type_card_out, TypeCardOut)
    assert type_card_out.id == 3
    assert type_card_out.type == "Student"

# Prueba: Verificar que el método from_dict falle con datos inválidos
def test_type_card_out_from_dict_invalid():
    with pytest.raises(TypeError):
        TypeCardOut.from_dict("invalid data")

# Prueba: Verificar el nombre de la entidad en TypeCardCreate
def test_type_card_create_entity_name():
    assert TypeCardCreate.__entity_name__ == "tipotarjeta"

# Prueba: Verificar el nombre de la entidad en TypeCardOut
def test_type_card_out_entity_name():
    assert TypeCardOut.__entity_name__ == "tipotarjeta"