import pytest
from datetime import datetime
from backend.app.models.maintainance import MaintenanceCreate, MaintenanceOut

def test_maintenance_create_to_dict():
    dt = datetime(2024, 5, 3, 10, 30)
    m = MaintenanceCreate(id=1, type="Preventivo", date=dt, id_unit=10, id_status=2)
    assert m.to_dict() == {"id": 1, "type": "Preventivo", "date": dt,"id_unit":10,"id_status":2}

def test_maintenance_get_fields():
    expected = {
        "id": "INTEGER PRIMARY KEY",
        "type": "TEXT",
        "date": "DATE",
        "id_unit": "INTEGER",
        "id_status": "INTEGER"
    }
    assert MaintenanceCreate.get_fields() == expected

def test_maintenance_out_from_dict():
    dt = datetime(2024, 6, 1, 8, 0)
    data = {
        "id": 5,
        "type": "Correctivo",
        "date": dt,
        "id_unit": 20,
        "id_status": 1
    }
    m = MaintenanceOut.from_dict(data)
    assert isinstance(m, MaintenanceOut)
    assert m.id == 5
    assert m.type == "Correctivo"
    assert m.date == dt
    assert m.id_unit == 20
    assert m.id_status == 1
