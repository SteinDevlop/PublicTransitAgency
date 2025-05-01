import unittest
from backend.app.models.incidence import IncidenceCreate

class TestIncidence(unittest.TestCase):

    def setUp(self):
        self.incidence_data = {
            "descripcion": "Descripción de la incidencia",
            "tipo": "Tipo de incidencia",
            "ticket_id": 10
        }
        self.incidence = IncidenceCreate(**self.incidence_data)

    def test_initial_values(self):
        self.assertEqual(self.incidence.descripcion, "Descripción de la incidencia")
        self.assertEqual(self.incidence.tipo, "Tipo de incidencia")
        self.assertEqual(self.incidence.ticket_id, 10)

    def test_setters(self):
        self.incidence.descripcion = "Nueva descripción"
        self.incidence.tipo = "Nuevo tipo"
        self.incidence.ticket_id = 20

        self.assertEqual(self.incidence.descripcion, "Nueva descripción")
        self.assertEqual(self.incidence.tipo, "Nuevo tipo")
        self.assertEqual(self.incidence.ticket_id, 20)

    def test_to_dict(self):
        expected_dict = {
            "descripcion": "Descripción de la incidencia",
            "tipo": "Tipo de incidencia",
            "ticket_id": 10
        }
        self.assertEqual(self.incidence.to_dict(), expected_dict)

    def test_get_fields(self):
        expected_fields = {
            "incidencia_id": "INTEGER PRIMARY KEY",
            "descripcion": "TEXT NOT NULL",
            "tipo": "TEXT",
            "ticket_id": "INTEGER NOT NULL"
        }
        self.assertEqual(IncidenceCreate.get_fields(), expected_fields)

if __name__ == "__main__":
    unittest.main()
