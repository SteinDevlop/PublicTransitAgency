import unittest
from src.backend.app.logic.incidence import Incidence
from src.backend.app.logic.ticket import Ticket

class TestIncidence(unittest.TestCase):

    def setUp(self):
        self.ticket = Ticket(status_code=1, ID="TICKET001")
        self.incidence = Incidence(
            description="Descripción inicial",
            type="Tipo inicial",
            status=self.ticket,
            incidence_id=1
        )

    def test_initial_values(self):
        self.assertEqual(self.incidence.description, "Descripción inicial")
        self.assertEqual(self.incidence.type, "Tipo inicial")
        self.assertEqual(self.incidence.status, self.ticket)
        self.assertEqual(self.incidence.incidence_id, 1)

    def test_setters(self):
        new_ticket = Ticket(status_code=2, ID="TICKET002")
        self.incidence.description = "Nueva descripción"
        self.incidence.type = "Nuevo tipo"
        self.incidence.status = new_ticket
        self.incidence.incidence_id = 2

        self.assertEqual(self.incidence.description, "Nueva descripción")
        self.assertEqual(self.incidence.type, "Nuevo tipo")
        self.assertEqual(self.incidence.status, new_ticket)
        self.assertEqual(self.incidence.incidence_id, 2)

    def test_update_incidence(self):
        new_ticket = Ticket(status_code=3, ID="TICKET003")
        self.incidence.update_incidence(
            description="Descripción actualizada",
            type="Tipo actualizado",
            status=new_ticket,
            incidence_id=3
        )

        self.assertEqual(self.incidence.description, "Descripción actualizada")
        self.assertEqual(self.incidence.type, "Tipo actualizado")
        self.assertEqual(self.incidence.status, new_ticket)
        self.assertEqual(self.incidence.incidence_id, 3)

    def test_update_incidence_without_id(self):
        new_ticket = Ticket(status_code=3, ID="TICKET003")
        with self.assertRaises(ValueError) as context:
            self.incidence.update_incidence(
                description="Descripción fallida",
                type="Tipo fallido",
                status=new_ticket,
                incidence_id=None
            )
        self.assertEqual(str(context.exception), "Incidence ID is required.")

if __name__ == "__main__":
    unittest.main()