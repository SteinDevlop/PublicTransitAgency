from fastapi import APIRouter, HTTPException
from logic.shift import Shift
from logic.schedule import Schedule
from logic.unit_transport import Transport
from logic.user_driver import UserDriver
from logic import universal_controller_json
import datetime

router = APIRouter()
controller = universal_controller_json()

@router.post("/shifts")
def create_shift(shift_data: dict):
    try:
        unit_data = shift_data.get("unit")
        if not unit_data:
            raise HTTPException(status_code=400, detail="Unit data is required")
        unit = Transport.from_dict(unit_data)

        schedule_data = shift_data.get("schedule")
        if not schedule_data:
            raise HTTPException(status_code=400, detail="Schedule data is required")
        schedule = Schedule.from_dict(schedule_data)

        driver_data = shift_data.get("driver")
        if not driver_data:
            raise HTTPException(status_code=400, detail="Driver data is required")
        driver = UserDriver.from_dict(driver_data)

        shift = Shift(
            unit=unit,
            start_time=datetime.datetime.fromisoformat(shift_data["start_time"]),
            end_time=datetime.datetime.fromisoformat(shift_data["end_time"]),
            driver=driver,
            schedule=schedule
        )

        shift.shift_assigment()

        controller.add(shift)
        return {"message": "Turno creado exitosamente"}

    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except KeyError as ke:
        raise HTTPException(status_code=422, detail=f"Falta el campo: {ke}")
