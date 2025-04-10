import unittest
from datetime import datetime
from src.backend.app.logic.mantainment import Maintenance

class TestMaintenance(unittest.TestCase):
    def setUp(self):
        self.maintenance = Maintenance(id=1, unit='Bus 101', date=datetime(2025, 5, 10), type='Oil Change', status='Scheduled')

    def test_schedule_maintenance(self):
        new_date = datetime(2025, 6, 15)
        self.maintenance.schedule_maintenance(new_date)
        self.assertEqual(self.maintenance.date, new_date)

    def test_update_status(self):
        self.maintenance.update_status('Completed')
        self.assertEqual(self.maintenance.status, 'Completed')
    
    def test_maintenance_attributes(self):
        self.assertEqual(self.maintenance.id, 1)
        self.assertEqual(self.maintenance.unit, 'Bus 101')
        self.assertEqual(self.maintenance.date, datetime(2025, 5, 10))
        self.assertEqual(self.maintenance.type, 'Oil Change')
        self.assertEqual(self.maintenance.status, 'Scheduled')

if __name__ == '__main__':
    unittest.main()
