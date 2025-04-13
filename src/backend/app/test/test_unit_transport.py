import unittest
from unittest.mock import patch
from src.backend.app.logic.unit_transport import Transport

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
        with patch('sys.stdout') as mocked_stdout:
            self.transport.send_alert("Low fuel")
            mocked_stdout.write.assert_called_with("Alert for Transport ID 1: Low fuel\n")

if __name__ == "__main__":
    unittest.main()
