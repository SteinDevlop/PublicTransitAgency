import unittest
from backend.app.logic.ticket import Ticket
from backend.app.logic.incidence import Incidence

class TestIncidence(unittest.TestCase):
    def setUp(self):
        # Crear un objeto Ticket para usar en los tests
        self.ticket = Ticket(status_code=1, ID="T123")
        # Crear un objeto Incidence para usar en los tests
        self.incidence = Incidence(
            ID=1,
            description="Test description",
            status=self.ticket,
            type="Test type",
            transport_id=123
        )

    def test_initialization(self):
        # Verificar que los atributos se inicializan correctamente
        self.assertEqual(self.incidence._ID, 1)
        self.assertEqual(self.incidence.description, "Test description")
        self.assertEqual(self.incidence.status, self.ticket)
        self.assertEqual(self.incidence.type, "Test type")
        self.assertEqual(self.incidence._transport_id, 123)

    def test_update_incidence(self):
        # Crear un nuevo objeto Ticket para actualizar el estado
        new_ticket = Ticket(status_code=2, ID="T456")
        # Actualizar la incidencia
        self.incidence.update_incidence(
            description="Updated description",
            status=new_ticket,
            type="Updated type",
            incidence_id=2
        )
        # Verificar que los atributos se actualizan correctamente
        self.assertEqual(self.incidence.description, "Updated description")
        self.assertEqual(self.incidence.status, new_ticket)
        self.assertEqual(self.incidence.type, "Updated type")
        self.assertEqual(self.incidence.incidence_id, 2)

    def test_update_incidence_without_id(self):
        # Intentar actualizar la incidencia sin un ID debe lanzar un ValueError
        with self.assertRaises(ValueError) as context:
            self.incidence.update_incidence(
                description="New description",
                status=self.ticket,
                type="New type",
                incidence_id=None
            )
        self.assertEqual(str(context.exception), "Incidence ID is required.")

if __name__ == "__main__":
    unittest.main()