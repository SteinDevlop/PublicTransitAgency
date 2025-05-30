import pytest
import datetime
from backend.app.logic.shift import Shift
from backend.app.logic.unit_transport import Transport
from backend.app.logic.schedule import Schedule
from backend.app.logic.user_driver import Worker

@pytest.fixture
def setup_shift():
    """
    Fixture para configurar un turno de prueba.
    """
    unit = Transport(unit_id="123", capacity=50)
    driver = Worker(name="John Doe", license_number="ABC123")
    schedule = Schedule(schedule_id="456", route="Route A", is_active=True)
    start_time = datetime.datetime.now() + datetime.timedelta(hours=1)
    end_time = start_time + datetime.timedelta(hours=4)
    return Shift(unit=unit, start_time=start_time, end_time=end_time, driver=driver, schedule=schedule)

def test_shift_assigment_success(setup_shift):
    """
    Prueba para asignar un turno exitosamente.
    """
    shift = setup_shift
    shift.unit.is_available = lambda start, end: True
    shift.schedule.is_valid = lambda: True
    assert shift.shift_assigment() is True

def test_shift_assigment_start_time_in_past(setup_shift):
    """
    Prueba para manejar un error cuando el tiempo de inicio está en el pasado.
    """
    shift = setup_shift
    shift.start_time = datetime.datetime.now() - datetime.timedelta(hours=1)
    with pytest.raises(ValueError, match="Start time cannot be in the past."):
        shift.shift_assigment()

def test_shift_assigment_end_time_before_start_time(setup_shift):
    """
    Prueba para manejar un error cuando el tiempo de fin es antes del tiempo de inicio.
    """
    shift = setup_shift
    shift.end_time = shift.start_time - datetime.timedelta(hours=1)
    with pytest.raises(ValueError, match="End time must be after start time."):
        shift.shift_assigment()

def test_shift_assigment_unit_not_available(setup_shift):
    """
    Prueba para manejar un error cuando la unidad no está disponible.
    """
    shift = setup_shift
    shift.unit.is_available = lambda start, end: False
    with pytest.raises(ValueError, match="Unit is not available for the specified time."):
        shift.shift_assigment()

def test_shift_assigment_invalid_schedule(setup_shift):
    """
    Prueba para manejar un error cuando el horario no es válido.
    """
    shift = setup_shift
    shift.schedule.is_valid = lambda: False
    with pytest.raises(ValueError, match="Schedule is not valid."):
        shift.shift_assigment()

def test_shift_change_success(setup_shift):
    """
    Prueba para cambiar un turno exitosamente.
    """
    shift = setup_shift
    shift.unit.is_available = lambda start, end: True
    new_start_time = shift.start_time + datetime.timedelta(hours=2)
    new_end_time = new_start_time + datetime.timedelta(hours=4)
    assert shift.shift_change(new_start_time, new_end_time) is True

def test_shift_change_start_time_in_past(setup_shift):
    """
    Prueba para manejar un error cuando el nuevo tiempo de inicio está en el pasado.
    """
    shift = setup_shift
    new_start_time = datetime.datetime.now() - datetime.timedelta(hours=1)
    new_end_time = new_start_time + datetime.timedelta(hours=4)
    with pytest.raises(ValueError, match="Start time cannot be in the past."):
        shift.shift_change(new_start_time, new_end_time)

def test_shift_change_end_time_before_start_time(setup_shift):
    """
    Prueba para manejar un error cuando el nuevo tiempo de fin es antes del nuevo tiempo de inicio.
    """
    shift = setup_shift
    new_start_time = shift.start_time + datetime.timedelta(hours=2)
    new_end_time = new_start_time - datetime.timedelta(hours=1)
    with pytest.raises(ValueError, match="End time must be after start time."):
        shift.shift_change(new_start_time, new_end_time)

def test_shift_change_unit_not_available(setup_shift):
    """
    Prueba para manejar un error cuando la unidad no está disponible para el nuevo turno.
    """
    shift = setup_shift
    shift.unit.is_available = lambda start, end: False
    new_start_time = shift.start_time + datetime.timedelta(hours=2)
    new_end_time = new_start_time + datetime.timedelta(hours=4)
    with pytest.raises(ValueError, match="Unit is not available for the specified time."):
        shift.shift_change(new_start_time, new_end_time)