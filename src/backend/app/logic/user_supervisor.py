from backend.app.logic.user import User
from backend.app.logic.card_operative import CardOperative
from backend.app.logic.user_driver import Worker
from backend.app.logic.reports import Reports
import json
import os

class Supervisor(User):
    def __init__(self, id_user:int, type_identification:str, identification:int, name:str, email:str, password:str,
                  role:str, card: CardOperative):
        super().__init__(id_user, type_identification, identification, name, email, password, role, card)

        if not self.verify_name(name):
            raise ValueError("Invalid Name")
        if not self.verify_email(email):
            raise ValueError("Invalid Email")
        if not self.verify_password(password):
            raise ValueError("Invalid Password")

    def get_driver_assignment(self, driver:Worker):
        """
        Purpose: Get information about the routes assigned to a driver.

        Args:
            driver (Driver): The driver whose route information is requested.

        Returns:
            list: List of assignments (routes) assigned to the driver.
        """
        return driver.get_driver_assigment()

    def create_driver_assignment_report(self, driver):
        """
        Purpose: Create a report of the routes assigned to a driver.

        Args:
            driver (Driver): The driver for whom the report is created.

        Returns:
            str: Path to the generated report file.
        """
        assignments = self.get_driver_assignment(driver)
        
        report_data = {
            "driver_id": driver.id_driver,
            "driver_name": driver.name,
            "assignments": assignments
        }
        new_report= Reports("Driver Assignment Report", driver.id_driver, json.dumps(report_data))
        return new_report.generate_report()
        
    def set_driver_assignment(self, driver, new_assignment):
        """
        Purpose: Update the route assignment information for a driver.

        Args:
            driver (Driver): The driver whose assignment information will be updated.
            new_assignment (dict): A dictionary representing the new assignment.

        Returns:
            bool: True if the update was successful, False otherwise.
        """
        if not isinstance(new_assignment, dict):
            raise ValueError("New assignment must be a dictionary")

        driver.assignments.append(new_assignment)
        return True
