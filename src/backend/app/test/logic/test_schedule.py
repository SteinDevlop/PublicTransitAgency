import unittest
import datetime
from backend.app.logic.schedule import Schedule
from backend.app.logic.transport_route import Route  # Clase dummy o real

class DummyRoute:
    def __init__(self, name="Route A"):
        self.name = name

    def __eq__(self, other):
        return isinstance(other, DummyRoute) and self.name == other.name

class TestScheduleClass(unittest.TestCase):
    """
    Unit tests for the Schedule class.
    """

    def setUp(self):
        """
        Set up a default Schedule instance before each test.
        """
        self.arrival = datetime.datetime(2025, 4, 15, 8, 0)
        self.departure = datetime.datetime(2025, 4, 15, 10, 0)
        self.route = DummyRoute()
        self.schedule = Schedule("SCH001", self.arrival, self.departure, self.route)

    def test_initial_values(self):
        self.assertEqual(self.schedule.schedule_id, "SCH001")
        self.assertEqual(self.schedule.arrival_date, self.arrival)
        self.assertEqual(self.schedule.departure_date, self.departure)
        self.assertEqual(self.schedule.route, self.route)

    def test_setters(self):
        new_arrival = datetime.datetime(2025, 4, 16, 9, 0)
        new_departure = datetime.datetime(2025, 4, 16, 11, 0)
        new_route = DummyRoute("Route B")

        self.schedule.schedule_id = "SCH002"
        self.schedule.arrival_date = new_arrival
        self.schedule.departure_date = new_departure
        self.schedule.route = new_route

        self.assertEqual(self.schedule.schedule_id, "SCH002")
        self.assertEqual(self.schedule.arrival_date, new_arrival)
        self.assertEqual(self.schedule.departure_date, new_departure)
        self.assertEqual(self.schedule.route, new_route)

if __name__ == "__main__":
    unittest.main()
