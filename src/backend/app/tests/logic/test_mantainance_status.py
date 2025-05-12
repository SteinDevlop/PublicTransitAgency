import pytest
from backend.app.logic.maintainance_status import MaintainanceStatus

def test_maintainance_status_initialization():
    status = MaintainanceStatus(id=1, unit="Unit 1", type="Preventive", status="Pending")
    assert status.id == 1
    assert status.unit == "Unit 1"
    assert status.type == "Preventive"
    assert status.status == "Pending"

def test_maintainance_status_setters():
    status = MaintainanceStatus(id=1, unit="Unit 1", type="Preventive", status="Pending")
    status.id = 2
    status.unit = "Unit 2"
    status.type = "Corrective"
    status.status = "Completed"

    assert status.id == 2
    assert status.unit == "Unit 2"
    assert status.type == "Corrective"
    assert status.status == "Completed"