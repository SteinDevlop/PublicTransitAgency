import pytest
from pydantic import ValidationError
from backend.app.models.movement import MovementCreate, MovementOut

@pytest.fixture
def sample_movement_data():
    return {
        "id": 1,
        "idtype": 1,
        "amount": 2000.75
    }

def test_movement_create_initialization(sample_movement_data):
    """Verifica que MovementCreate se inicialice correctamente."""
    movement = MovementCreate(**sample_movement_data)
    assert movement.id == sample_movement_data["id"]
    assert movement.idtype == sample_movement_data["idtype"]
    assert movement.amount == sample_movement_data["amount"]

def test_movement_create_invalid_data():
    """Verifica que MovementCreate genere un error con datos inválidos."""
    with pytest.raises(ValidationError):
        MovementCreate(id="invalid", type="wrong", amount="not_a_float")

def test_movement_to_dict(sample_movement_data):
    """Verifica que to_dict devuelve el diccionario correcto."""
    movement = MovementCreate(**sample_movement_data)
    assert movement.to_dict() == sample_movement_data

def test_movement_get_fields():
    """Verifica que get_fields devuelve la estructura esperada."""
    expected_fields = {
        "id": "INTEGER PRIMARY KEY",
        "idtype": "INTEGER",
        "amount": "FLOAT"
    }
    assert MovementCreate.get_fields() == expected_fields

def test_movement_out_initialization(sample_movement_data):
    """Verifica que MovementOut se inicialice correctamente."""
    movement_out = MovementOut(**sample_movement_data)
    assert movement_out.id == sample_movement_data["id"]
    assert movement_out.idtype == sample_movement_data["idtype"]
    assert movement_out.amount == sample_movement_data["amount"]

def test_movement_out_from_dict():
    """Verifica que from_dict inicializa correctamente un objeto MovementOut."""
    data = {"id": 2, "idtype": 2, "amount": 3500.50}
    movement_out = MovementOut.from_dict(data)
    assert isinstance(movement_out, MovementOut)
    assert movement_out.id == 2
    assert movement_out.idtype == 2
    assert movement_out.amount == 3500.50
