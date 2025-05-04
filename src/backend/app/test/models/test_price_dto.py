import pytest
from pydantic import ValidationError
from backend.app.models.price import PriceCreate, PriceOut

@pytest.fixture
def sample_price_data():
    return {
        "id": 1,
        "unidadtransportype": 2,
        "amount": 1500.50
    }

def test_price_create_initialization(sample_price_data):
    """Verifica que PriceCreate se inicialice correctamente."""
    price = PriceCreate(**sample_price_data)
    assert price.id == sample_price_data["id"]
    assert price.unidadtransportype == sample_price_data["unidadtransportype"]
    assert price.amount == sample_price_data["amount"]

def test_price_create_invalid_data():
    """Verifica que PriceCreate genere un error con datos inválidos."""
    with pytest.raises(ValidationError):
        PriceCreate(id="invalid", unidadtransportype="wrong", amount="not_a_float")

def test_price_to_dict(sample_price_data):
    """Verifica que to_dict devuelve el diccionario correcto."""
    price = PriceCreate(**sample_price_data)
    assert price.to_dict() == sample_price_data

def test_price_get_fields():
    """Verifica que get_fields devuelve la estructura esperada."""
    expected_fields = {
        "id": "INTEGER PRIMARY KEY",
        "unidadtransportype": "INTEGER",
        "amount": "FLOAT"
    }
    assert PriceCreate.get_fields() == expected_fields

def test_price_out_initialization(sample_price_data):
    """Verifica que PriceOut se inicialice correctamente."""
    price_out = PriceOut(**sample_price_data)
    assert price_out.id == sample_price_data["id"]
    assert price_out.unidadtransportype == sample_price_data["unidadtransportype"]
    assert price_out.amount == sample_price_data["amount"]

def test_price_out_from_dict():
    """Verifica que from_dict inicializa correctamente un objeto PriceOut."""
    data = {"id": 2, "unidadtransportype": 3, "amount": 2500.75}
    price_out = PriceOut.from_dict(data)
    assert isinstance(price_out, PriceOut)
    assert price_out.id == 2
    assert price_out.unidadtransportype == 3
    assert price_out.amount == 2500.75
