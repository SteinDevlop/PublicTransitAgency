import unittest
from typing import List
from backend.app.logic.transport_parade import Parade
from backend.app.logic.transport_route import Route

class MockParade:
    """
    Mock class for Parade to use in testing.
    """
    def __init__(self, name: str):
        self.name = name

class TestRoute(unittest.TestCase):
    def setUp(self):
        """
        Sets up test cases with mock Parade objects.
        """
        self.parade1 = MockParade("Stop1")
        self.parade2 = MockParade("Stop2")
        self.route = Route(stops=[self.parade1, self.parade2], estimated_duration=45.0, origin="City A", destination="City B")
    
    def test_initialization(self):
        """
        Test that Route initializes correctly.
        """
        self.assertEqual(len(self.route.stops), 2)
        self.assertEqual(self.route.estimated_duration, 45.0)
        self.assertEqual(self.route.origin, "City A")
        self.assertEqual(self.route.destination, "City B")

    def test_update_route(self):
        """
        Test updating different attributes of Route.
        """
        parade3 = MockParade("Stop3")
        self.route.update_route(stops=[parade3], estimated_duration=30.0, origin="City X", destination="City Y")
        
        self.assertEqual(len(self.route.stops), 1)
        self.assertEqual(self.route.stops[0].name, "Stop3")
        self.assertEqual(self.route.estimated_duration, 30.0)
        self.assertEqual(self.route.origin, "City X")
        self.assertEqual(self.route.destination, "City Y")
    
    def test_partial_update(self):
        """
        Test updating only some attributes of Route.
        """
        self.route.update_route(estimated_duration=60.0)
        
        self.assertEqual(len(self.route.stops), 2)  # Stops should remain unchanged
        self.assertEqual(self.route.estimated_duration, 60.0)
        self.assertEqual(self.route.origin, "City A")  # Origin should remain unchanged
        self.assertEqual(self.route.destination, "City B")  # Destination should remain unchanged

if __name__ == "__main__":
    unittest.main()
