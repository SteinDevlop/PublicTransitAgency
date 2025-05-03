from backend.app.logic.user import User
from backend.app.logic.card_operative import CardOperative
from backend.app.logic.reports import Reports
from backend.app.logic.unit_transport import Transport
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

        self.manteinment_report = []
        self.schedule = []

    def create_report(self, unit_transport:Transport, report_details:str):
        """
        Purpose: Create a maintenance report.
        """
        report_data = {
            "unit_transport_id": unit_transport.id,
            "unit_transport_type": unit_transport.type,
            "comments": report_details
        }
        new_report = Reports("Maintenance Report", unit_transport.id, json.dumps(report_data))
        report_path = new_report.generate_report()

        
        self.manteinment_report.append(report_data)

        return report_path

    def create_schedule(self, schedule_details: dict):
        """
        Purpose: Create a maintenance schedule.
        Args:
            schedule_details (dict): Details of the maintenance schedule.
        """
        self.schedule.append(schedule_details)
        print("Maintenance schedule created successfully.")


    def get_manteinment_schedule(self):
        """
        Purpose: Get schedule information.
        Returns:
            dict: The current maintenance schedule.
        """
        return self.schedule

    def set_manteinment_report(self, report_index: int, attribute: str, value):
        """
        Purpose: Update a maintenance report.
        Args:
            report_index (int): Index of the report in the list.
            attribute (str): Attribute to update.
            value: New value for the attribute.
        """
        try:
            self.manteinment_report[report_index][attribute] = value
            print(f"Report attribute '{attribute}' updated successfully.")
        except IndexError:
            print(f"Report at index '{report_index}' not found.")
        except KeyError:
            print(f"Attribute '{attribute}' not found in the report.")

