import pytest
from pydantic import ValidationError
from backend.app.models.type_movement import TypeMovementCreate, TypeMovementOut

@pytest.fixture
def sample_type_movement_data():
    return {
        "id": 1,
        "type": "Entrada"
    }

def test_type_movement_create_initialization(sample_type_movement_data):
    """Verifica que TypeMovementCreate se inicialice correctamente."""
    tm = TypeMovementCreate(**sample_type_movement_data)
    assert tm.id == sample_type_movement_data["id"]
    assert tm.type == sample_type_movement_data["type"]

def test_type_movement_create_invalid_data():
    """Verifica que TypeMovementCreate genere un error con datos inválidos."""
    with pytest.raises(ValidationError):
        TypeMovementCreate(id="invalid", type=123)

def test_type_movement_to_dict(sample_type_movement_data):
    """Verifica que to_dict devuelve el diccionario correcto."""
    tm = TypeMovementCreate(**sample_type_movement_data)
    assert tm.to_dict() == sample_type_movement_data

def test_type_movement_get_fields():
    """Verifica que get_fields devuelve la estructura esperada."""
    expected_fields = {
        "id": "INTEGER PRIMARY KEY",
        "type": "varchar(20)"
    }
    assert TypeMovementCreate.get_fields() == expected_fields

def test_type_movement_out_initialization(sample_type_movement_data):
    """Verifica que TypeMovementOut se inicialice correctamente."""
    tm_out = TypeMovementOut(**sample_type_movement_data)
    assert tm_out.id == sample_type_movement_data["id"]
    assert tm_out.type == sample_type_movement_data["type"]

def test_type_movement_out_from_dict():
    """Verifica que from_dict inicializa correctamente un objeto TypeMovementOut."""
    data = {"id": 2, "type": "Salida"}
    tm_out = TypeMovementOut.from_dict(data)
    assert isinstance(tm_out, TypeMovementOut)
    assert tm_out.id == 2
    assert tm_out.type == "Salida"
