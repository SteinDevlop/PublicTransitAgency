import unittest
from backend.app.logic.type_card import TypeCard

class TestTypeCard(unittest.TestCase):

    def test_typecard_creation(self):
        tc = TypeCard(1, "Standard")
        self.assertEqual(tc.id, 1)
        self.assertEqual(tc.type, "Standard")

    def test_typecard_str_representation(self):
        tc = TypeCard(2, "Student")
        expected = str({"id": 2, "type": "Student"})
        self.assertEqual(str(tc), expected)

    def test_typecard_setters(self):
        tc = TypeCard(0, "")
        tc.id = 10
        tc.type = "Senior"

        self.assertEqual(tc.id, 10)
        self.assertEqual(tc.type, "Senior")

if __name__ == "__main__":
    unittest.main()
