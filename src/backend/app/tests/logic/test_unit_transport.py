import unittest
from backend.app.logic.ticket import Ticket
from backend.app.logic.unit_transport import Transport

class TestTransport(unittest.TestCase):
    def setUp(self):
        # Crear un objeto Ticket para usar en los tests
        self.ticket = Ticket(status_code=1, ID="T123")
        # Crear un objeto Transport para usar en los tests
        self.transport = Transport(
            id="TR001",
            type="Bus",
            status=self.ticket,
            ubication="Downtown",
            capacity=50
        )

    def test_initialization(self):
        # Verificar que los atributos se inicializan correctamente
        self.assertEqual(self.transport.id, "TR001")
        self.assertEqual(self.transport.type, "Bus")
        self.assertEqual(self.transport.status, self.ticket)
        self.assertEqual(self.transport.ubication, "Downtown")
        self.assertEqual(self.transport.capacity, 50)

    def test_update_transport(self):
        # Crear un nuevo objeto Ticket para actualizar el estado
        new_ticket = Ticket(status_code=2, ID="T456")
        # Actualizar los atributos del transporte
        self.transport.id = "TR002"
        self.transport.type = "Train"
        self.transport.status = new_ticket
        self.transport.ubication = "Uptown"
        self.transport.capacity = 100

        # Verificar que los atributos se actualizan correctamente
        self.assertEqual(self.transport.id, "TR002")
        self.assertEqual(self.transport.type, "Train")
        self.assertEqual(self.transport.status, new_ticket)
        self.assertEqual(self.transport.ubication, "Uptown")
        self.assertEqual(self.transport.capacity, 100)

    def test_ticket_integration(self):
        # Verificar que el estado del ticket está correctamente integrado
        self.assertEqual(self.transport.status.status_code, 1)
        self.assertEqual(self.transport.status._ID, "T123")

if __name__ == "__main__":
    unittest.main()