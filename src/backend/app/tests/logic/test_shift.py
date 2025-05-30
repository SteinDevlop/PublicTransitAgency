import unittest
import datetime
from unittest.mock import MagicMock
from backend.app.logic.shift import Shift

class DummyTransport:
    def __init__(self, unit_id="T1"):
        self.unit_id = unit_id
    def is_available(self, start, end):
        return True

class DummySchedule:
    def is_valid(self):
        return True

class DummyDriver:
    def __str__(self):
        return "Driver1"

class TestShift(unittest.TestCase):
    def setUp(self):
        self.unit = DummyTransport()
        self.driver = DummyDriver()
        self.schedule = DummySchedule()
        self.start_time = datetime.datetime.now() + datetime.timedelta(hours=1)
        self.end_time = self.start_time + datetime.timedelta(hours=2)
        self.shift = Shift(
            unit=self.unit,
            start_time=self.start_time,
            end_time=self.end_time,
            driver=self.driver,
            schedule=self.schedule
        )

    def test_shift_assignment_success(self):
        self.assertTrue(self.shift.shift_assigment())

    def test_shift_assignment_start_time_in_past(self):
        self.shift.start_time = datetime.datetime.now() - datetime.timedelta(hours=1)
        with self.assertRaises(ValueError) as cm:
            self.shift.shift_assigment()
        self.assertIn("Start time cannot be in the past.", str(cm.exception))

    def test_shift_assignment_end_time_before_start_time(self):
        self.shift.end_time = self.shift.start_time - datetime.timedelta(minutes=1)
        with self.assertRaises(ValueError) as cm:
            self.shift.shift_assigment()
        self.assertIn("End time must be after start time.", str(cm.exception))

    def test_shift_assignment_unit_not_available(self):
        self.shift.unit.is_available = MagicMock(return_value=False)
        with self.assertRaises(ValueError) as cm:
            self.shift.shift_assigment()
        self.assertIn("Unit is not available for the specified time.", str(cm.exception))

    def test_shift_assignment_invalid_schedule(self):
        self.shift.schedule.is_valid = MagicMock(return_value=False)
        with self.assertRaises(ValueError) as cm:
            self.shift.shift_assigment()
        self.assertIn("Schedule is not valid.", str(cm.exception))

    def test_shift_change_success(self):
        new_start = self.start_time + datetime.timedelta(hours=3)
        new_end = new_start + datetime.timedelta(hours=2)
        self.assertTrue(self.shift.shift_change(new_start, new_end))
        self.assertEqual(self.shift.start_time, new_start)
        self.assertEqual(self.shift.end_time, new_end)

    def test_shift_change_start_time_in_past(self):
        new_start = datetime.datetime.now() - datetime.timedelta(hours=2)
        new_end = new_start + datetime.timedelta(hours=1)
        with self.assertRaises(ValueError) as cm:
            self.shift.shift_change(new_start, new_end)
        self.assertIn("Start time cannot be in the past.", str(cm.exception))

    def test_shift_change_end_time_before_start_time(self):
        new_start = self.start_time + datetime.timedelta(hours=1)
        new_end = new_start - datetime.timedelta(minutes=10)
        with self.assertRaises(ValueError) as cm:
            self.shift.shift_change(new_start, new_end)
        self.assertIn("End time must be after start time.", str(cm.exception))

    def test_shift_change_unit_not_available(self):
        self.shift.unit.is_available = MagicMock(return_value=False)
        new_start = self.start_time + datetime.timedelta(hours=1)
        new_end = new_start + datetime.timedelta(hours=1)
        with self.assertRaises(ValueError) as cm:
            self.shift.shift_change(new_start, new_end)
        self.assertIn("Unit is not available for the specified time.", str(cm.exception))

if __name__ == "__main__":
    unittest.main()