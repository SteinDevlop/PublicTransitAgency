import unittest
from logic.routes import Routes

class TestRoutes(unittest.TestCase):
    def setUp(self):
        self.sample_route = {
            "route_id": "R1",
            "name": "Ruta Centro",
            "stops": ["Stop1", "Stop2", "Stop3"]
        }
        self.route = Routes(self.sample_route, "R1")

    def test_initial_route(self):
        self.assertEqual(self.route.route, self.sample_route)
        self.assertEqual(self.route.route_id, "R1")

    def test_set_route(self):
        new_route = {
            "route_id": "R2",
            "name": "Ruta Norte",
            "stops": ["StopA", "StopB"]
        }
        self.route.route = new_route
        self.assertEqual(self.route.route, new_route)
        self.assertEqual(self.route.route_id, "R2")

    def test_set_route_id(self):
        self.route.route_id = "R3"
        self.assertEqual(self.route.route_id, "R3")

if __name__ == "__main__":
    unittest.main()
