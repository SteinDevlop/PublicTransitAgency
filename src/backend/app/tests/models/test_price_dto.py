import pytest
from pydantic import ValidationError
from backend.app.models.price import PriceCreate, PriceOut

@pytest.fixture
def sample_price_data():
    return {
        "ID": 1,
        "IDTipoTransporte": 2,
        "Monto": 1500.50
    }

def test_price_create_initialization(sample_price_data):
    """Verifica que PriceCreate se inicialice correctamente."""
    price = PriceCreate(**sample_price_data)
    assert price.ID == sample_price_data["ID"]
    assert price.IDTipoTransporte == sample_price_data["IDTipoTransporte"]
    assert price.Monto == sample_price_data["Monto"]

def test_price_create_invalid_data():
    """Verifica que PriceCreate genere un error con datos inválidos."""
    with pytest.raises(ValidationError):
        PriceCreate(ID="invalid", IDTipoTransporte="wrong", Monto="not_a_float")

def test_price_to_dict(sample_price_data):
    """Verifica que to_dict devuelve el diccionario correcto."""
    price = PriceCreate(**sample_price_data)
    assert price.to_dict() == sample_price_data

def test_price_get_fields():
    """Verifica que get_fields devuelve la estructura esperada."""
    expected_fields = {
        "ID": "INTEGER PRIMARY KEY",
        "IDTipoTransporte": "INTEGER",
        "Monto": "FLOAT"
    }
    assert PriceCreate.get_fields() == expected_fields

def test_price_out_initialization(sample_price_data):
    """Verifica que PriceOut se inicialice correctamente."""
    price_out = PriceOut(**sample_price_data)
    assert price_out.ID == sample_price_data["ID"]
    assert price_out.IDTipoTransporte == sample_price_data["IDTipoTransporte"]
    assert price_out.Monto == sample_price_data["Monto"]

def test_price_out_from_dict():
    """Verifica que from_dict inicializa correctamente un objeto PriceOut."""
    data = {"ID": 2, "IDTipoTransporte": 3, "Monto": 2500.75}
    price_out = PriceOut.from_dict(data)
    assert isinstance(price_out, PriceOut)
    assert price_out.ID == 2
    assert price_out.IDTipoTransporte == 3
    assert price_out.Monto == 2500.75
