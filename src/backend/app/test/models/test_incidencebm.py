import unittest
from backend.app.models.incidence import Incidence

class TestIncidence(unittest.TestCase):
    def setUp(self):
        self.incidence = Incidence(
            ID=1,
            IDTicket=101,
            Descripcion="Broken window",
            Tipo="Mechanical",
            IDUnidad=5
        )

    def test_initialization(self):
        self.assertEqual(self.incidence.ID, 1)
        self.assertEqual(self.incidence.IDTicket, 101)
        self.assertEqual(self.incidence.Descripcion, "Broken window")
        self.assertEqual(self.incidence.Tipo, "Mechanical")
        self.assertEqual(self.incidence.IDUnidad, 5)

    def test_to_dict(self):
        incidence_dict = self.incidence.to_dict()
        self.assertEqual(incidence_dict["ID"], 1)
        self.assertEqual(incidence_dict["IDTicket"], 101)
        self.assertEqual(incidence_dict["Descripcion"], "Broken window")
        self.assertEqual(incidence_dict["Tipo"], "Mechanical")
        self.assertEqual(incidence_dict["IDUnidad"], 5)

    def test_get_fields(self):
        fields = Incidence.get_fields()
        self.assertIn("ID", fields)
        self.assertIn("IDTicket", fields)
        self.assertIn("Descripcion", fields)
        self.assertIn("Tipo", fields)
        self.assertIn("IDUnidad", fields)

if __name__ == "__main__":
    unittest.main()