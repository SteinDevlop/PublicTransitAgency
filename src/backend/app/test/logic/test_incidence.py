<<<<<<< HEAD
=======
import unittest
from backend.app.models.incidence import IncidenceCreate

class TestIncidence(unittest.TestCase):

    def setUp(self):
        self.incidence_data = {
            "Descripcion": "Descripción de la incidencia",
            "Tipo": "Tipo de incidencia",
            "TicketID": 10
        }
        self.incidence = IncidenceCreate(**self.incidence_data)

    def test_initial_values(self):
        self.assertEqual(self.incidence.Descripcion, "Descripción de la incidencia")
        self.assertEqual(self.incidence.Tipo, "Tipo de incidencia")
        self.assertEqual(self.incidence.TicketID, 10)

    def test_setters(self):
        self.incidence.Descripcion = "Nueva descripción"
        self.incidence.Tipo = "Nuevo tipo"
        self.incidence.TicketID = 20

        self.assertEqual(self.incidence.Descripcion, "Nueva descripción")
        self.assertEqual(self.incidence.Tipo, "Nuevo tipo")
        self.assertEqual(self.incidence.TicketID, 20)

    def test_to_dict(self):
        expected_dict = {
            "Descripcion": "Descripción de la incidencia",
            "Tipo": "Tipo de incidencia",
            "TicketID": 10
        }
        self.assertEqual(self.incidence.to_dict(), expected_dict)

    def test_get_fields(self):
        expected_fields = {
            "IncidenciaID": "INTEGER PRIMARY KEY",
            "Descripcion": "TEXT NOT NULL",
            "Tipo": "TEXT",
            "TicketID": "INTEGER NOT NULL"
        }
        self.assertEqual(IncidenceCreate.get_fields(), expected_fields)

if __name__ == "__main__":
    unittest.main()
>>>>>>> d9ce6cb (Rewind)
