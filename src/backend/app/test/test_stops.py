import unittest
from src.backend.app.logic.stops import Stops

class TestStopsClass(unittest.TestCase):
    def setUp(self):
        self.stop_data = {"stop_id": "S001", "name": "Main Street"}
        self.stops = Stops(self.stop_data, id="S001")

    def test_initial_values(self):
        self.assertEqual(self.stops.stop, self.stop_data)
        self.assertEqual(self.stops.stop_id, "S001")

    def test_stop_setter_updates_stop_id(self):
        new_data = {"stop_id": "S002", "name": "Central Ave"}
        self.stops.stop = new_data
        self.assertEqual(self.stops.stop, new_data)
        self.assertEqual(self.stops.stop_id, "S002")

    def test_stop_id_setter(self):
        self.stops.stop_id = "NEWID"
        self.assertEqual(self.stops.stop_id, "NEWID")

if __name__ == "__main__":
    unittest.main()
