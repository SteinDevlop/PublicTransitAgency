import unittest
from src.backend.app.services.unit_transport import Transport

class TestTransport(unittest.TestCase):
    def setUp(self):
        self.transport = Transport(id=1, type="Truck", status="Active", ubication="Warehouse", capacity=1000)
    
    def test_initialization(self):
        self.assertEqual(self.transport.id, 1)
        self.assertEqual(self.transport.type, "Truck")
        self.assertEqual(self.transport.status, "Active")
        self.assertEqual(self.transport.ubication, "Warehouse")
        self.assertEqual(self.transport.capacity, 1000)
    
    def test_actualize_status(self):
        self.transport.actualize_status("Inactive")
        self.assertEqual(self.transport.status, "Inactive")
    
    def test_send_alert(self):
        with self.assertLogs() as captured:
            self.transport.send_alert("Low fuel")
            self.assertIn("Alert for Transport ID 1: Low fuel", captured.output[0])

if __name__ == "__main__":
    unittest.main()