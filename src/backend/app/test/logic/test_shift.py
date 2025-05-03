import unittest
import datetime
from backend.app.logic.user_driver import Worker
from backend.app.logic.shift import Shift
class DummyTransport:
    def __init__(self, id="T001"):
        self.id = id

    def __eq__(self, other):
        return isinstance(other, DummyTransport) and self.id == other.id

class DummySchedule:
    def __init__(self, name="S001"):
        self.name = name

    def __eq__(self, other):
        return isinstance(other, DummySchedule) and self.name == other.name

class DummyWorker(Worker):
    def __init__(self, name="John Doe"):
        self.name = name

    def __eq__(self, other):
        return isinstance(other, DummyWorker) and self.name == other.name

class TestShiftClass(unittest.TestCase):
    def setUp(self):
        self.unit = DummyTransport()
        self.schedule = DummySchedule()
        self.start_time = datetime.datetime(2025, 4, 12, 8, 0)
        self.end_time = datetime.datetime(2025, 4, 12, 12, 0)
        self.driver = DummyWorker(name="John Doe")  # Use DummyWorker instead of string
        self.shift = Shift(self.unit, self.start_time, self.end_time, self.driver, self.schedule)

    def test_initial_values(self):
        self.assertEqual(self.shift.unit, self.unit)
        self.assertEqual(self.shift.start_time, self.start_time)
        self.assertEqual(self.shift.end_time, self.end_time)
        self.assertEqual(self.shift.driver, self.driver)
        self.assertEqual(self.shift.schedule, self.schedule)

    def test_setters(self):
        new_unit = DummyTransport("T002")
        new_schedule = DummySchedule("S002")
        new_start = datetime.datetime(2025, 4, 13, 10, 0)
        new_end = datetime.datetime(2025, 4, 13, 14, 0)
        new_driver = DummyWorker(name="Jane Smith")  # Use DummyWorker instead of string

        self.shift.unit = new_unit
        self.shift.start_time = new_start
        self.shift.end_time = new_end
        self.shift.driver = new_driver  # Use DummyWorker
        self.shift.schedule = new_schedule

        self.assertEqual(self.shift.unit, new_unit)
        self.assertEqual(self.shift.start_time, new_start)
        self.assertEqual(self.shift.end_time, new_end)
        self.assertEqual(self.shift.driver, new_driver)  # Updated test
        self.assertEqual(self.shift.schedule, new_schedule)

if __name__ == "__main__":
    unittest.main()
