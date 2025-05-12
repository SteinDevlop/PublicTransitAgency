import pytest
from backend.app.logic.user_supervisor import Supervisor
from backend.app.logic.card_operative import CardOperative
from backend.app.logic.user_driver import Worker
from backend.app.logic.reports import Reports
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
        # Solo imprimir
        print(f"Generating report: {self.type_report}, Data: {self.generated_data}")

def mock_card():
    return MagicMock()

# Test Supervisor
def test_create_driver_assignment_report(monkeypatch, capsys):
    # Setup
    supervisor = Supervisor(1, "DNI", 12345678, "John Doe", "john@example.com", "Password@123", "supervisor", mock_card())
    
    driver = FakeDriver(10, "Jane Driver")
    driver.assignments.append({"route": "A1", "shift": "Morning"})
    driver.assignments.append({"route": "B2", "shift": "Evening"})

    # Parchar la clase Reports para usar FakeReport
    monkeypatch.setattr("backend.app.logic.user_supervisor.Reports", FakeReport)

    # Exercise
    supervisor.create_driver_assignment_report(driver)

    # Capture print output
    captured = capsys.readouterr()

    # Verify (solo verificamos que se imprimió algo esperado)
    assert "Generating report: Driver Assignment Report" in captured.out
    assert '"driver_name": "Jane Driver"' in captured.out
    assert '"route": "A1"' in captured.out

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
