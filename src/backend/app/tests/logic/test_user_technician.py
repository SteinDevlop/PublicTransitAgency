import unittest
from backend.app.logic.user_technician import Technician
from backend.app.logic.card_operative import CardOperative
from backend.app.logic.unit_transport import Transport
from backend.app.logic.reports import Reports
from unittest.mock import MagicMock

def mock_card():
    return MagicMock()

class FakeReport(Reports):
    def __init__(self, type_report, driver_id, generated_data):
        self.type_report = type_report
        self.driver_id = driver_id
        self.generated_data = generated_data

    def generate_report(self):
        # Solo imprimir
        print(f"Generating report: {self.type_report}, Data: {self.generated_data}")

class TestTechnician(unittest.TestCase):
    
    def setUp(self):
        # Creamos objetos necesarios para el técnico
        self.card = mock_card()
        self.technician = Technician(
            id_user=1,
            type_identification="DNI",
            identification=12345678,
            name="Alice",
            email="alice@example.com",
            password="Secure@Pass123",
            role="technician",
            card=self.card
        )
        self.unit_transport = Transport(
            id=101,
            type="Bus",
            ubication="Garage A",
            status="Available",
            capacity=50
        )

    def test_create_report(self):
        report_details = "Routine maintenance completed."
        report_path = self.technician.create_report(self.unit_transport, report_details)
        
        # Verificar que el reporte se creó y almacenó
        self.assertTrue(len(self.technician.manteinment_report) > 0)
        self.assertIn("comments", self.technician.manteinment_report[0])
        self.assertEqual(self.technician.manteinment_report[0]["comments"], report_details)
        self.assertIsInstance(True,bool)

    def test_create_schedule(self):
        schedule_details = {
            "Monday": "Check brakes",
            "Tuesday": "Oil change"
        }
        self.technician.create_schedule(schedule_details)
        
        # Verificar que el cronograma se creó
        self.assertTrue(len(self.technician.schedule) > 0)
        self.assertEqual(self.technician.schedule[0]["Monday"], "Check brakes")

    def test_set_manteinment_report(self):
        report_details = "Initial maintenance done."
        self.technician.create_report(self.unit_transport, report_details)
        
        # Modificar el comentario del reporte
        self.technician.set_manteinment_report(0, "comments", "Updated maintenance comment.")
        
        # Verificar el cambio
        updated_comment = self.technician.manteinment_report[0]["comments"]
        self.assertEqual(updated_comment, "Updated maintenance comment.")

if __name__ == "__main__":
    unittest.main()
