import pytest
from datetime import datetime
from backend.app.models.maintainance import MaintenanceCreate, MaintenanceOut

# Prueba: Crear un mantenimiento correctamente
def test_maintenance_create():
    fecha = datetime(2024, 1, 1, 12, 0, 0)
    maintenance = MaintenanceCreate(ID=1, id_status=2, type="Preventive", fecha=fecha, idunidad=10)

    assert maintenance.ID == 1
    assert maintenance.id_status == 2
    assert maintenance.type == "Preventive"
    assert maintenance.fecha == fecha
    assert maintenance.idunidad == 10

# Prueba: Crear un mantenimiento con valores por defecto
def test_maintenance_create_defaults():
    maintenance = MaintenanceCreate()

    assert maintenance.ID is None
    assert maintenance.id_status is None
    assert maintenance.type is None
    assert maintenance.fecha is None
    assert maintenance.idunidad is None

# Prueba: Conversión a diccionario con to_dict
def test_maintenance_to_dict():
    fecha = datetime(2024, 5, 10, 14, 30, 0)
    maintenance = MaintenanceCreate(ID=2, id_status=1, type="Corrective", fecha=fecha, idunidad=5)
    maintenance_dict = maintenance.to_dict()

    assert isinstance(maintenance_dict, dict)
    assert maintenance_dict == {
        "ID": 2,
        "id_status": 1,
        "type": "Corrective",
        "fecha": fecha,
        "idunidad": 5
    }

# Prueba: Obtener campos del modelo
def test_maintenance_get_fields():
    expected_fields = {
        "ID": "INTEGER PRIMARY KEY",
        "id_status": "INTEGER",
        "type": "varchar(100)",
        "fecha": "DATE",
        "idunidad": "INTEGER"
    }
    assert MaintenanceCreate.get_fields() == expected_fields

# Prueba: Crear una instancia de MaintenanceOut desde un diccionario
def test_maintenance_out_from_dict():
    fecha = datetime(2024, 7, 15, 9, 0, 0)
    data = {
        "ID": 3,
        "id_status": 3,
        "type": "Inspection",
        "fecha": fecha,
        "idunidad": 20
    }
    maintenance_out = MaintenanceOut.from_dict(data)

    assert isinstance(maintenance_out, MaintenanceOut)
    assert maintenance_out.ID == 3
    assert maintenance_out.id_status == 3
    assert maintenance_out.type == "Inspection"
    assert maintenance_out.fecha == fecha
    assert maintenance_out.idunidad == 20

# Prueba: Verificar el nombre de la entidad en MaintenanceCreate
def test_maintenance_create_entity_name():
    assert MaintenanceCreate.__entity_name__ == "mantenimientoins"

# Prueba: Verificar el nombre de la entidad en MaintenanceOut
def test_maintenance_out_entity_name():
    assert MaintenanceOut.__entity_name__ == "mantenimientoins"