import unittest
from src.backend.app.logic.incidence import Incidence

class TestIncidence(unittest.TestCase):
    """
    Unit tests for the Incidence class.
    """

    def setUp(self):
        """
        Set up a default Incidence instance before each test.
        """
        self.incidence = Incidence("Puerta rota", "Mecánica", "Abierta", 101)

    def test_initial_values(self):
        """
        Test that initial values are set correctly.
        """ 
        self.assertEqual(self.incidence.description, "Puerta rota")
        self.assertEqual(self.incidence.type, "Mecánica")
        self.assertEqual(self.incidence.status, "Abierta")
        self.assertEqual(self.incidence.incidence_id, 101)

    def test_setters_update_values(self):
        """
        Test that setters update values correctly.
        """
        self.incidence.description = "Falla en frenos"
        self.incidence.type = "Seguridad"
        self.incidence.status = "Cerrada"
        self.incidence.incidence_id = 202

        self.assertEqual(self.incidence.description, "Falla en frenos")
        self.assertEqual(self.incidence.type, "Seguridad")
        self.assertEqual(self.incidence.status, "Cerrada")
        self.assertEqual(self.incidence.incidence_id, 202)

    def test_update_incidence_method(self):
        """
        Test that update_incidence updates fields correctly.
        """
        self.incidence.update_incidence("Motor dañado", "Mecánica", "Pendiente", 101)
        self.assertEqual(self.incidence.description, "Motor dañado")
        self.assertEqual(self.incidence.type, "Mecánica")
        self.assertEqual(self.incidence.status, "Pendiente")

    def test_update_incidence_without_id_raises_error(self):
        """
        Test that update_incidence raises ValueError if ID is missing.
        """
        with self.assertRaises(ValueError):
            self.incidence.update_incidence("Error", "Tipo", "Status", None)

if __name__ == "__main__":
    unittest.main()
