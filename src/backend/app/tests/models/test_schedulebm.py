import unittest
from backend.app.models.schedule import Schedule

class TestSchedule(unittest.TestCase):
    def setUp(self):
        self.schedule = Schedule(ID=1, Llegada="08:00", Salida="09:00")

    def test_initialization(self):
        self.assertEqual(self.schedule.ID, 1)
        self.assertEqual(self.schedule.Llegada, "08:00")
        self.assertEqual(self.schedule.Salida, "09:00")

    def test_to_dict(self):
        schedule_dict = self.schedule.to_dict()
        self.assertEqual(schedule_dict["ID"], 1)
        self.assertEqual(schedule_dict["Llegada"], "08:00")
        self.assertEqual(schedule_dict["Salida"], "09:00")

    def test_get_fields(self):
        fields = Schedule.get_fields()
        self.assertIn("ID", fields)
        self.assertIn("Llegada", fields)
        self.assertIn("Salida", fields)

if __name__ == "__main__":
    unittest.main()