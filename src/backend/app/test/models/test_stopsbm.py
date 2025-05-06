"""import unittest
from backend.app.models.stops import Stop

class TestStop(unittest.TestCase):
    def setUp(self):
        self.stop = Stop(ID=1, Nombre="Central Stop", Ubicacion="Downtown")

    def test_initialization(self):
        self.assertEqual(self.stop.ID, 1)
        self.assertEqual(self.stop.Nombre, "Central Stop")
        self.assertEqual(self.stop.Ubicacion, "Downtown")

    def test_to_dict(self):
        stop_dict = self.stop.to_dict()
        self.assertEqual(stop_dict["ID"], 1)
        self.assertEqual(stop_dict["Nombre"], "Central Stop")
        self.assertEqual(stop_dict["Ubicacion"], "Downtown")

    def test_get_fields(self):
        fields = Stop.get_fields()
        self.assertIn("ID", fields)
        self.assertIn("Nombre", fields)
        self.assertIn("Ubicacion", fields)

if __name__ == "__main__":
    unittest.main()
    """