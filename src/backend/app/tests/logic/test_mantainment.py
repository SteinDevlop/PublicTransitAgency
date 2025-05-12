import unittest
from datetime import datetime
from backend.app.logic.mantainment import Maintenance

class TestMaintenance(unittest.TestCase):

    def test_maintenance_creation(self):
        now = datetime.now()
        m = Maintenance(1, 101, 2, "Preventive", now)
        
        self.assertEqual(m.id, 1)
        self.assertEqual(m.id_unit, 101)
        self.assertEqual(m.id_status, 2)
        self.assertEqual(m.type, "Preventive")
        self.assertEqual(m.date, now)

    def test_maintenance_str_representation(self):
        now = datetime(2023, 1, 1, 12, 0)
        m = Maintenance(2, 202, 3, "Corrective", now)

        expected = str({
            "id": 2,
            "id_unit": 202,
            "id_status": 3,
            "type": "Corrective",
            "date": now.isoformat()
        })

        self.assertEqual(str(m), expected)

    def test_maintenance_setters(self):
        m = Maintenance(0, 0, 0, "", datetime.now())
        m.id = 5
        m.id_unit = 500
        m.id_status = 1
        m.type = "Emergency"
        new_date = datetime(2024, 5, 20)
        m.date = new_date

        self.assertEqual(m.id, 5)
        self.assertEqual(m.id_unit, 500)
        self.assertEqual(m.id_status, 1)
        self.assertEqual(m.type, "Emergency")
        self.assertEqual(m.date, new_date)

if __name__ == "__main__":
    unittest.main()


