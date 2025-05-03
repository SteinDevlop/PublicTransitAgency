import unittest
from backend.app.models.routes import Route

class TestRoute(unittest.TestCase):
    def setUp(self):
        self.route = Route(ID=1, IDHorario=2, Nombre="Route A")

    def test_initialization(self):
        self.assertEqual(self.route.ID, 1)
        self.assertEqual(self.route.IDHorario, 2)
        self.assertEqual(self.route.Nombre, "Route A")

    def test_to_dict(self):
        route_dict = self.route.to_dict()
        self.assertEqual(route_dict["ID"], 1)
        self.assertEqual(route_dict["IDHorario"], 2)
        self.assertEqual(route_dict["Nombre"], "Route A")

    def test_get_fields(self):
        fields = Route.get_fields()
        self.assertIn("ID", fields)
        self.assertIn("IDHorario", fields)
        self.assertIn("Nombre", fields)

if __name__ == "__main__":
    unittest.main()