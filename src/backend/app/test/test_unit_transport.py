import unittest
from src.backend.app.logic.unit_transport import Transport

class TestTransport(unittest.TestCase):

    def setUp(self):
        # Este método se ejecuta antes de cada test
        self.transport = Transport(id=1, type="Truck", status="Active", ubication="Location A", capacity=100)

    def test_initial_values(self):
        # Verificamos los valores iniciales de la clase
        self.assertEqual(self.transport.id, 1)
        self.assertEqual(self.transport.type, "Truck")
        self.assertEqual(self.transport.status, "Active")
        self.assertEqual(self.transport.ubication, "Location A")
        self.assertEqual(self.transport.capacity, 100)

    def test_setter_getter_id(self):
        # Probamos el setter y getter de 'id'
        self.transport.id = 2
        self.assertEqual(self.transport.id, 2)

    def test_setter_getter_type(self):
        # Probamos el setter y getter de 'type'
        self.transport.type = "Bus"
        self.assertEqual(self.transport.type, "Bus")

    def test_setter_getter_status(self):
        # Probamos el setter y getter de 'status'
        self.transport.status = "Inactive"
        self.assertEqual(self.transport.status, "Inactive")

    def test_setter_getter_ubication(self):
        # Probamos el setter y getter de 'ubication'
        self.transport.ubication = "Location B"
        self.assertEqual(self.transport.ubication, "Location B")

    def test_setter_getter_capacity(self):
        # Probamos el setter y getter de 'capacity'
        self.transport.capacity = 120
        self.assertEqual(self.transport.capacity, 120)

if __name__ == "__main__":
    unittest.main()
