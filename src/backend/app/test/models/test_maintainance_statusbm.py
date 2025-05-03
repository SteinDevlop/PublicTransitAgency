import unittest
from backend.app.models.maintainance_status import MaintainanceStatus

class TestMaintainanceStatus(unittest.TestCase):
    def setUp(self):
        self.status = MaintainanceStatus(
            id=1,
            unit="Unit A",
            type="Mechanical",
            status="Pending"
        )

    def test_initialization(self):
        self.assertEqual(self.status.id, 1)
        self.assertEqual(self.status.unit, "Unit A")
        self.assertEqual(self.status.type, "Mechanical")
        self.assertEqual(self.status.status, "Pending")

    def test_to_dict(self):
        status_dict = self.status.to_dict()
        self.assertEqual(status_dict["id"], 1)
        self.assertEqual(status_dict["unit"], "Unit A")
        self.assertEqual(status_dict["type"], "Mechanical")
        self.assertEqual(status_dict["status"], "Pending")

    def test_get_fields(self):
        fields = MaintainanceStatus.get_fields()
        self.assertIn("id", fields)
        self.assertIn("unit", fields)
        self.assertIn("type", fields)
        self.assertIn("status", fields)

if __name__ == "__main__":
    unittest.main()