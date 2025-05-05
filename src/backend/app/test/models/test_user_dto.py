import pytest
from pydantic import ValidationError
from backend.app.models.user import UserCreate, UserOut  # Asegúrate de cambiar "your_module" por el nombre real del archivo donde están las clases

@pytest.fixture
def sample_user_data():
    return {
        "id": 1,
        "identification": 12345678,
        "name": "Andrés",
        "lastname": "Pérez",
        "email": "andres@example.com",
        "password": "securepassword",
        "idtype_user": 2,
        "idturn": 3
    }

def test_user_create_initialization(sample_user_data):
    """Verifica que UserCreate se inicialice correctamente con datos válidos."""
    user = UserCreate(**sample_user_data)
    assert user.id == sample_user_data["id"]
    assert user.name == sample_user_data["name"]
    assert user.email == sample_user_data["email"]

def test_user_create_invalid_data():
    """Verifica que UserCreate genera un error cuando los datos no cumplen con los tipos esperados."""
    with pytest.raises(ValidationError):
        UserCreate(id="invalid", identification="not_a_number", name=123, lastname=456, email=789, password=None, idtype_user="wrong", idturn="fail")

def test_to_dict_method(sample_user_data):
    """Verifica que el método to_dict retorna los datos correctamente."""
    user = UserCreate(**sample_user_data)
    user_dict = user.to_dict()
    assert user_dict == sample_user_data

def test_get_fields_method():
    """Verifica que get_fields devuelve la estructura esperada de la base de datos."""
    expected_fields = {
            "id": "INTEGER PRIMARY KEY",
            "identification": "INTEGER",
            "name": "VARCHAR(100)",
            "lastname": "VARCHAR(100)",
            "email": "VARCHAR(100)",
            "password": "VARCHAR(100)",
            "idtype_user": "INTEGER",
            "idturn": "INTEGER"
    }
    assert UserCreate.get_fields() == expected_fields

def test_user_out_initialization(sample_user_data):
    """Verifica que UserOut se inicialice correctamente con los datos de UserCreate."""
    user_out = UserOut(**sample_user_data)
    assert user_out.name == sample_user_data["name"]
    assert user_out.email == sample_user_data["email"]

def test_user_out_from_dict(sample_user_data):
    """Verifica que from_dict inicializa correctamente un objeto UserOut."""
    user_out = UserOut.from_dict(sample_user_data)
    assert isinstance(user_out, UserOut)
    assert user_out.name == sample_user_data["name"]

