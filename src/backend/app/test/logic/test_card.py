import pytest
from backend.app.logic.card import Card

# Clase concreta de prueba que NO empieza con 'Test'
class ConcreteCard(Card):
    """
    Concrete subclass of Card used for unit testing.
    Implements the abstract use_card method.
    """
    def use_card(self):
        return "Card used"

# Fixture para configurar la tarjeta antes de cada prueba
@pytest.fixture
def test_card():
    return ConcreteCard(1234, "TestType", 100.0)

# Prueba: valores iniciales de la tarjeta
def test_initial_values(test_card):
    assert test_card.id_card == 1234
    assert test_card.card_type == "TestType"
    assert test_card.balance == 100.0

# Prueba: actualización de valores mediante setters
def test_setters(test_card):
    test_card.id_card = 4321
    test_card.card_type = "UpdatedType"
    test_card.balance = 50.0

    assert test_card.id_card == 4321
    assert test_card.card_type == "UpdatedType"
    assert test_card.balance == 50.0

# Prueba: el saldo no puede ser negativo
def test_balance_cannot_be_negative(test_card):
    with pytest.raises(ValueError):
        test_card.balance = -10.0

# Prueba: representación en cadena (__str__)
def test_str_representation(test_card):
    expected = "{'idn': 1234, 'tipo': 'TestType', 'saldo': 100.0}"
    assert str(test_card) == expected

# Prueba: uso de la tarjeta en la subclase
def test_use_card_method(test_card):
    assert test_card.use_card() == "Card used"

# Prueba: error al instanciar la clase abstracta
def test_abstract_class_instantiation_raises_error():
    class Dummy(Card):
        pass

    with pytest.raises(NotImplementedError):
        Dummy(1111, "DummyType", 0.0).use_card()
