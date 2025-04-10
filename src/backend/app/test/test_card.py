import unittest
from src.backend.app.logic.card import Card

class TestCard(Card):
    """
    Concrete test subclass of Card used for unit testing.
    Implements the abstract use_card method.
    """
    def use_card(self):
        return "Card used"


class TestCardClass(unittest.TestCase):
    """
    Unit tests for the Card class and its behavior using a test subclass.
    """

    def setUp(self):
        """
        Set up a default TestCard instance before each test.
        """
        self.card = TestCard(1234, "TestType", 100.0)

    def test_initial_values(self):
        """
        Test that the initial values are set correctly.
        """
        self.assertEqual(self.card.id_card, 1234)
        self.assertEqual(self.card.card_type, "TestType")
        self.assertEqual(self.card.balance, 100.0)

    def test_setters(self):
        """
        Test that setters update the values correctly.
        """
        self.card.id_card = 4321
        self.card.card_type = "UpdatedType"
        self.card.balance = 50.0

        self.assertEqual(self.card.id_card, 4321)
        self.assertEqual(self.card.card_type, "UpdatedType")
        self.assertEqual(self.card.balance, 50.0)

    def test_balance_cannot_be_negative(self):
        """
        Test that setting a negative balance raises a ValueError.
        """
        with self.assertRaises(ValueError):
            self.card.balance = -10.0

    def test_str_representation(self):
        """
        Test the __str__ method returns the correct string representation.
        """
        expected = "Card(id_card=1234, card_type='TestType', balance=100.00)"
        self.assertEqual(str(self.card), expected)

    def test_use_card_method(self):
        """
        Test that the use_card method works in the subclass.
        """
        self.assertEqual(self.card.use_card(), "Card used")

    def test_abstract_class_instantiation_raises_error(self):
        """
        Test that calling use_card on the abstract Card class raises NotImplementedError.
        """
        class Dummy(Card):
            pass

        with self.assertRaises(NotImplementedError):
            Dummy(1111, "DummyType", 0.0).use_card()


if __name__ == "__main__":
    unittest.main()