from src.backend.app.logic.user import User
from src.backend.app.logic.card_operative import CardOperative
from src.backend.app.logic.reports import Reports
from src.backend.app.logic.unit_transport import UnitTransport
import json
import os

class Technician(User):
    def __init__(self, id_user:int, type_identification:str, identification:int, name:str, email:str, password:str, 
                 role:str, card:CardOperative):
        super().__init__(id_user, type_identification, identification, name, email, password, role,card)
                
        if not self.verify_name(name):
            raise ValueError("Invalid Name")
        if not self.verify_email(email):
            raise ValueError("Invalid Email")
        if not self.verify_password(password):
            raise ValueError("Invalid Password")

        # Inicializamos atributos específicos de Technician
        self.manteinment_report = []
        self.schedule = []

    def create_report(self, unit_transport:UnitTransport , report_details:str):
        """
        Purpose: Create a maintenance report.}
        Args:
            report_details (dict): Details of the maintenance report.
        """
        report_data = {
            "unit_transport_id": unit_transport.id_unit_transport,
            "unit_transport_type": unit_transport.type_unit_transport,
            "comments": report_details
        }
        new_report= Reports("Maintenace Report", unit_transport.id_unit_transport, json.dumps(report_details))
        return new_report.generate_report()

    def get_manteinment_schedule(self):
        """
        Purpose: Get schedule information.
        Returns:
            dict: The current maintenance schedule.
        """
        return self.schedule

    def set_manteinment_report(self, attribute, value):
        """
        Purpose: Update a maintenance report.
        Args:
            attribute (str): The attribute of the report to update.
            value: The new value for the attribute.
        """
        if attribute in self.manteinment_report:
            self.manteinment_report[attribute] = value
            print(f"Report attribute '{attribute}' updated successfully.")
        else:
            print(f"Attribute '{attribute}' not found in the report.")
