import unittest
from src.backend.app.logic.incidence import Incidence
from src.backend.app.logic.ticket import Ticket

class TestIncidence(unittest.TestCase):

    def setUp(self):
        self.ticket = Ticket(status_code=1, ID="TICKET001")
        self.incidence = Incidence(description="Descripción inicial", status=self.ticket, type="Choque", incidence_id=1)

    def test_initial_values(self):
        self.assertEqual(self.incidence.description, "Descripción inicial")
        self.assertEqual(self.incidence.status, self.ticket)
        self.assertEqual(self.incidence.type, "Choque")
        self.assertEqual(self.incidence.incidence_id, 1)

    def test_update_incidence(self):
        new_ticket = Ticket(status_code=2, ID="TICKET002")
        self.incidence.update_incidence(description="Actualizado", status=new_ticket, type="Nuevo tipo", incidence_id=2)
        self.assertEqual(self.incidence.description, "Actualizado")
        self.assertEqual(self.incidence.status, new_ticket)
        self.assertEqual(self.incidence.type, "Nuevo tipo")
        self.assertEqual(self.incidence.incidence_id, 2)

if __name__ == "__main__":
    unittest.main()
