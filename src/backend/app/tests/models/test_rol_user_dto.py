import pytest
from pydantic import ValidationError
from backend.app.models.rol_user import RolUserCreate, RolUserOut

@pytest.fixture
def sample_rol_user_data():
    return {
        "id": 1,
        "type": "Administrador"
    }

def test_rol_user_create_initialization(sample_rol_user_data):
    """Verifica que RolUserCreate se inicialice correctamente."""
    ru = RolUserCreate(**sample_rol_user_data)
    assert ru.id == sample_rol_user_data["id"]
    assert ru.type == sample_rol_user_data["type"]

def test_rol_user_create_invalid_data():
    """Verifica que RolUserCreate genere un error con datos inválidos."""
    with pytest.raises(ValidationError):
        RolUserCreate(id="invalid", type=123)

def test_rol_user_to_dict(sample_rol_user_data):
    """Verifica que to_dict devuelve el diccionario correcto."""
    ru = RolUserCreate(**sample_rol_user_data)
    assert ru.to_dict() == sample_rol_user_data

def test_rol_user_get_fields():
    """Verifica que get_fields devuelve la estructura esperada."""
    expected_fields = {
        "id": "INTEGER PRIMARY KEY",
        "type": "varchar(20)"
    }
    assert RolUserCreate.get_fields() == expected_fields

def test_rol_user_out_initialization(sample_rol_user_data):
    """Verifica que RolUserOut se inicialice correctamente."""
    ru_out = RolUserOut(**sample_rol_user_data)
    assert ru_out.id == sample_rol_user_data["id"]
    assert ru_out.type == sample_rol_user_data["type"]

def test_rol_user_out_from_dict():
    """Verifica que from_dict inicializa correctamente un objeto RolUserOut."""
    data = {"id": 2, "type": "Usuario"}
    ru_out = RolUserOut.from_dict(data)
    assert isinstance(ru_out, RolUserOut)
    assert ru_out.id == 2
    assert ru_out.type == "Usuario"
