from fastapi import APIRouter, Query
from logic.schedule import Schedule
from logic import universal_controller_json

router = APIRouter()
controller = universal_controller_json()

@router.get("/schedules")
def get_schedules(schedule_id: str = Query(default=None)):
    if schedule_id:
        schedule = controller.get_by_id(Schedule, schedule_id)
        if not schedule:
            return {"error": "Horario no encontrado"}
        return schedule.to_dict()
    else:
        all_schedules = controller.read_all(Schedule())
        return all_schedules