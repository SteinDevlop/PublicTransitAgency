import pytest
from src.backend.app.logic.user_supervisor import Supervisor
from src.backend.app.logic.card_operative import CardOperative
from src.backend.app.logic.user_driver import Worker
from src.backend.app.logic.reports import Reports
from unittest.mock import MagicMock

# Mocks o fakes
class FakeDriver(Worker):
    def __init__(self, id_driver, name):
        self.id_driver = id_driver
        self.name = name
        self.assignments = []

    def get_driver_assigment(self):
        return self.assignments

class FakeReport(Reports):
    def __init__(self, type_report, driver_id, generated_data):
        self.type_report = type_report
        self.driver_id = driver_id
        self.generated_data = generated_data

    def generate_report(self):
        print(f"Generating report: {self.type_report}, Data: {self.generated_data}")
        return True
def mock_card():
    return MagicMock()  # simulamos el CardOperative

# Test Supervisor
def test_create_driver_assignment_report(monkeypatch):
    # Setup
    supervisor = Supervisor(1, "DNI", 12345678, "John Doe", "john@example.com", "Password@123", "supervisor", mock_card())
    
    driver = FakeDriver(10, "Jane Driver")
    driver.assignments.append({"route": "A1", "shift": "Morning"})
    driver.assignments.append({"route": "B2", "shift": "Evening"})

    # Parchar la clase Reports para usar FakeReport
    monkeypatch.setattr("src.backend.app.logic.user_supervisor.Reports", FakeReport)

    # Exercise
    report_path = supervisor.create_driver_assignment_report(driver)

    # Verify
    assert report_path == "/fake/path/10_report.txt"

def test_set_driver_assignment_success():
    # Setup
    supervisor = Supervisor(1, "DNI", 12345678, "John Doe", "john@example.com", "Password@123", "supervisor", mock_card())  
    driver = FakeDriver(11, "Mark Driver")

    new_assignment = {"route": "C3", "shift": "Night"}

    # Exercise
    result = supervisor.set_driver_assignment(driver, new_assignment)

    # Verify
    assert result is True
    assert driver.assignments == [new_assignment]

def test_set_driver_assignment_invalid():
    # Setup
    supervisor = Supervisor(1, "DNI", 12345678, "John Doe", "john@example.com", "Password@123", "supervisor", mock_card())
    driver = FakeDriver(12, "Anna Driver")

    invalid_assignment = ["route", "shift"]

    # Exercise and Verify
    with pytest.raises(ValueError, match="New assignment must be a dictionary"):
        supervisor.set_driver_assignment(driver, invalid_assignment)
