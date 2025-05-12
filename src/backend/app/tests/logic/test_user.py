# test_user.py
import pytest
from backend.app.logic.user import User
from backend.app.logic.card import Card  # Esto es porque tu User recibe un Card

# Mock mínimo para el Card si no lo necesitas en las pruebas
class MockCard:
    pass

@pytest.fixture
def sample_user():
    return User(
        id_user=1,
        type_identification="DNI",
        identification=12345678,
        name="John Doe",
        email="john.doe@example.com",
        password="Test@123",
        role="user",
        card=MockCard()
    )

def test_update_name(sample_user):
    sample_user.update_information("name", "Jane Doe")
    assert sample_user.name == "Jane Doe"

def test_update_email(sample_user):
    sample_user.update_information("email", "jane.doe@example.com")
    assert sample_user.email == "jane.doe@example.com"

def test_update_password_valid(sample_user):
    sample_user.update_information("password", "Newpass@123")
    assert sample_user.password == "Newpass@123"

def test_update_invalid_name(sample_user):
    with pytest.raises(ValueError, match="Invalid Name"):
        sample_user.update_information("name", "Jane123")

def test_update_invalid_email(sample_user):
    with pytest.raises(ValueError, match="Invalid Email"):
        sample_user.update_information("email", "invalid-email")

def test_update_invalid_password(sample_user):
    with pytest.raises(ValueError, match="Invalid Password"):
        sample_user.update_information("password", "short")

def test_update_invalid_attribute(sample_user):
    with pytest.raises(ValueError, match="Not a Valid Attribute"):
        sample_user.update_information("invalid", "some_value")
