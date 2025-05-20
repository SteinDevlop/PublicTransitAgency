import pytest
from backend.app.models.type_card import TypeCardCreate, TypeCardOut

# Prueba: Crear un tipo de tarjeta correctamente
def test_type_card_create():
    type_card = TypeCardCreate(ID=1, Tipo="VIP")

    assert type_card.ID == 1
    assert type_card.Tipo == "VIP"

# Prueba: Crear un tipo de tarjeta con valores por defecto
def test_type_card_create_defaults():
    type_card = TypeCardCreate()

    assert type_card.ID is None
    assert type_card.Tipo is None

# Prueba: Conversión a diccionario con to_dict
def test_type_card_to_dict():
    type_card = TypeCardCreate(ID=2, Tipo="Regular")
    type_card_dict = type_card.to_dict()
    assert isinstance(type_card_dict, dict)
    assert type_card_dict == {
        "ID": 2,
        "Tipo": "Regular"
    }

# Prueba: Obtener campos del modelo
def test_type_card_get_fields():
    expected_fields = {
        "ID": "INTEGER PRIMARY KEY",
        "Tipo": "VARCHAR(20)"
    }
    assert TypeCardCreate.get_fields() == expected_fields

# Prueba: Crear una instancia de TypeCardOut desde un diccionario
def test_type_card_out_from_dict():
    data = {
        "ID": 3,
        "Tipo": "Student"
    }
    type_card_out = TypeCardOut.from_dict(data)

    assert isinstance(type_card_out, TypeCardOut)
    assert type_card_out.ID == 3
    assert type_card_out.Tipo == "Student"

# Prueba: Verificar que el método from_dict falle con datos inválidos
def test_type_card_out_from_dict_invalid():
    with pytest.raises(TypeError):
        TypeCardOut.from_dict("invalid data")

# Prueba: Verificar el nombre de la entidad en TypeCardCreate
def test_type_card_create_entity_name():
    assert TypeCardCreate._entity_name_ == "tipotarjeta"

# Prueba: Verificar el nombre de la entidad en TypeCardOut
def test_type_card_out_entity_name():
    assert TypeCardOut._entity_name_ == "tipotarjeta"