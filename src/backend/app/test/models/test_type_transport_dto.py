import pytest
from pydantic import ValidationError
from backend.app.models.type_transport import TypeTransportCreate, TypeTransportOut

@pytest.fixture
def sample_type_transport_data():
    return {
        "id": 1,
        "type": "Bus"
    }

def test_type_transport_create_initialization(sample_type_transport_data):
    """Verifica que TypeTransportCreate se inicialice correctamente."""
    tt = TypeTransportCreate(**sample_type_transport_data)
    assert tt.id == sample_type_transport_data["id"]
    assert tt.type == sample_type_transport_data["type"]

def test_type_transport_create_invalid_data():
    """Verifica que TypeTransportCreate genere un error con datos inválidos."""
    with pytest.raises(ValidationError):
        TypeTransportCreate(id="invalid", type=123)

def test_type_transport_to_dict(sample_type_transport_data):
    """Verifica que to_dict devuelve el diccionario correcto."""
    tt = TypeTransportCreate(**sample_type_transport_data)
    assert tt.to_dict() == sample_type_transport_data

def test_type_transport_get_fields():
    """Verifica que get_fields devuelve la estructura esperada."""
    expected_fields = {
        "id": "INTEGER PRIMARY KEY",
        "type": "varchar(20)"
    }
    assert TypeTransportCreate.get_fields() == expected_fields

def test_type_transport_out_initialization(sample_type_transport_data):
    """Verifica que TypeTransportOut se inicialice correctamente."""
    tt_out = TypeTransportOut(**sample_type_transport_data)
    assert tt_out.id == sample_type_transport_data["id"]
    assert tt_out.type == sample_type_transport_data["type"]

def test_type_transport_out_from_dict():
    """Verifica que from_dict inicializa correctamente un objeto TypeTransportOut."""
    data = {"id": 2, "type": "Train"}
    tt_out = TypeTransportOut.from_dict(data)
    assert isinstance(tt_out, TypeTransportOut)
    assert tt_out.id == 2
    assert tt_out.type == "Train"
