import unittest
from backend.app.models.transport import Transport

class TestTransport(unittest.TestCase):
    def setUp(self):
        self.transport = Transport(
            id=1,
            type="Bus",
            status="Active",
            ubication="Downtown",
            capacity=50
        )

    def test_initialization(self):
        self.assertEqual(self.transport.id, 1)
        self.assertEqual(self.transport.type, "Bus")
        self.assertEqual(self.transport.status, "Active")
        self.assertEqual(self.transport.ubication, "Downtown")
        self.assertEqual(self.transport.capacity, 50)

    def test_to_dict(self):
        transport_dict = self.transport.to_dict()
        self.assertEqual(transport_dict["id"], 1)
        self.assertEqual(transport_dict["type"], "Bus")
        self.assertEqual(transport_dict["status"], "Active")
        self.assertEqual(transport_dict["ubication"], "Downtown")
        self.assertEqual(transport_dict["capacity"], 50)

    def test_get_fields(self):
        fields = Transport.get_fields()
        self.assertIn("id", fields)
        self.assertIn("type", fields)
        self.assertIn("status", fields)
        self.assertIn("ubication", fields)
        self.assertIn("capacity", fields)

if __name__ == "__main__":
    unittest.main()