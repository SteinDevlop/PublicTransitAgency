import unittest
from src.backend.app.logic.maintainance_status import MaintainanceStatus

class TestMaintainanceStatus(unittest.TestCase):
    """
    Unit tests for the MaintainanceStatus class.
    """

    def setUp(self):
        """
        Set up a default MaintainanceStatus instance before each test.
        """
        self.status = MaintainanceStatus(1, "Bus-001", "Preventivo", "En proceso")

    def test_initial_values(self):
        """
        Test that initial values are set correctly.
        """
        self.assertEqual(self.status.id, 1)
        self.assertEqual(self.status.unit, "Bus-001")
        self.assertEqual(self.status.type, "Preventivo")
        self.assertEqual(self.status.status, "En proceso")

    def test_setters_update_values(self):
        """
        Test that the setters correctly update the values.
        """
        self.status.id = 2
        self.status.unit = "Bus-002"
        self.status.type = "Correctivo"
        self.status.status = "Completado"

        self.assertEqual(self.status.id, 2)
        self.assertEqual(self.status.unit, "Bus-002")
        self.assertEqual(self.status.type, "Correctivo")
        self.assertEqual(self.status.status, "Completado")

if __name__ == "__main__":
    unittest.main()
