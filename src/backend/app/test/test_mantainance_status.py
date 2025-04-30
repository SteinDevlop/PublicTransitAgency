import unittest
from backend.app.models.maintainance_status import MaintainanceStatusCreate

class TestMaintainanceStatus(unittest.TestCase):

    def setUp(self):
        self.status_data = {
            "ID": 1,
            "TipoEstado": "Pendiente",
            "UnidadTransporte": "Bus-123",
            "Status": "Activo"
        }
        self.status = MaintainanceStatusCreate(**self.status_data)

    def test_initial_values(self):
        self.assertEqual(self.status.ID, 1)
        self.assertEqual(self.status.TipoEstado, "Pendiente")
        self.assertEqual(self.status.UnidadTransporte, "Bus-123")
        self.assertEqual(self.status.Status, "Activo")

    def test_setters(self):
        self.status.ID = 2
        self.status.TipoEstado = "En Proceso"
        self.status.UnidadTransporte = "Bus-456"
        self.status.Status = "Inactivo"

        self.assertEqual(self.status.ID, 2)
        self.assertEqual(self.status.TipoEstado, "En Proceso")
        self.assertEqual(self.status.UnidadTransporte, "Bus-456")
        self.assertEqual(self.status.Status, "Inactivo")

    def test_to_dict(self):
        expected_dict = {
            "ID": 1,
            "TipoEstado": "Pendiente",
            "UnidadTransporte": "Bus-123",
            "Status": "Activo"
        }
        self.assertEqual(self.status.to_dict(), expected_dict)

    def test_get_fields(self):
        expected_fields = {
            "ID": "INTEGER PRIMARY KEY",
            "TipoEstado": "TEXT NOT NULL",
            "UnidadTransporte": "TEXT",
            "Status": "TEXT NOT NULL"
        }
        self.assertEqual(MaintainanceStatusCreate.get_fields(), expected_fields)

if __name__ == "__main__":
    unittest.main()