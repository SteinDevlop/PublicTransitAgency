import pytest
from pydantic import ValidationError
from backend.app.models.movement import MovementCreate, MovementOut

@pytest.fixture
def sample_movement_data():
    return {
        "ID": 1,
        "IDTipoMovimiento": 1,
        "Monto": 2000.75,
        "IDTarjeta":1
    }

def test_movement_create_initialization(sample_movement_data):
    """Verifica que MovementCreate se inicialice correctamente."""
    movement = MovementCreate(**sample_movement_data)
    assert movement.ID == sample_movement_data["ID"]
    assert movement.IDTipoMovimiento == sample_movement_data["IDTipoMovimiento"]
    assert movement.Monto == sample_movement_data["Monto"]

def test_movement_create_invalid_data():
    """Verifica que MovementCreate genere un error con datos inválidos."""
    with pytest.raises(ValidationError):
        MovementCreate(ID="invalid", type="wrong", Monto="not_a_float")

def test_movement_to_dict(sample_movement_data):
    """Verifica que to_dict devuelve el diccionario correcto."""
    movement = MovementCreate(**sample_movement_data)
    assert movement.to_dict() == sample_movement_data

def test_movement_get_fields():
    """Verifica que get_fields devuelve la estructura esperada."""
    expected_fields = {
        "ID": "INTEGER PRIMARY KEY",
        "IDTipoMovimiento": "INTEGER",
        "Monto": "FLOAT",
        "IDTarjeta":"Integer"
    }
    assert MovementCreate.get_fields() == expected_fields

def test_movement_out_initialization(sample_movement_data):
    """Verifica que MovementOut se inicialice correctamente."""
    movement_out = MovementOut(**sample_movement_data)
    assert movement_out.ID == sample_movement_data["ID"]
    assert movement_out.IDTipoMovimiento == sample_movement_data["IDTipoMovimiento"]
    assert movement_out.Monto == sample_movement_data["Monto"]

def test_movement_out_from_dict():
    """Verifica que from_dict inicializa correctamente un objeto MovementOut."""
    data = {"ID": 2, "IDTipoMovimiento": 2, "Monto": 3500.50,"IDTarjeta":1 }
    movement_out = MovementOut.from_dict(data)
    assert isinstance(movement_out, MovementOut)
    assert movement_out.ID == 2
    assert movement_out.IDTipoMovimiento == 2
    assert movement_out.Monto == 3500.50
    assert movement_out.IDTarjeta == 1
