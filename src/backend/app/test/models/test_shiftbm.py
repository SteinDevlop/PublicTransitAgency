import unittest
from backend.app.models.shift import Shift

class TestShift(unittest.TestCase):
    def setUp(self):
        self.shift = Shift(ID=1, TipoTurno="Diurno")

    def test_initialization(self):
        self.assertEqual(self.shift.ID, 1)
        self.assertEqual(self.shift.TipoTurno, "Diurno")

    def test_to_dict(self):
        shift_dict = self.shift.to_dict()
        self.assertEqual(shift_dict["ID"], 1)
        self.assertEqual(shift_dict["TipoTurno"], "Diurno")

    def test_get_fields(self):
        fields = Shift.get_fields()
        self.assertIn("ID", fields)
        self.assertIn("TipoTurno", fields)

if __name__ == "__main__":
    unittest.main()