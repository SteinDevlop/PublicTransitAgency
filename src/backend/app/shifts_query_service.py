from fastapi import APIRouter, Query
from logic.shift import Shift
from logic import universal_controller_json

router = APIRouter()
controller = universal_controller_json()

@router.get("/shifts")
def get_shifts(driver_id: str = Query(default=None)):
    all_shifts = controller.read_all(Shift())
    if driver_id:
        matched = [
            shift for shift in all_shifts
            if shift.get("driver", {}).get("driver_id") == driver_id
        ]
        return matched if matched else {"message": "No se encontraron turnos para ese conductor"}
    return all_shifts
