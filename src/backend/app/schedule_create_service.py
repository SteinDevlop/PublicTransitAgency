from fastapi import APIRouter, HTTPException
from logic.schedule import Schedule
from logic.routes import Route
from logic import universal_controller_json
import datetime

router = APIRouter()
controller = universal_controller_json()

@router.post("/schedules")
def create_schedule(schedule_data: dict):
    try:
        route_data = schedule_data.get("route")
        if not route_data:
            raise HTTPException(status_code=400, detail="Route data is required")
        route = Route.from_dict(route_data)

        schedule = Schedule(
            schedule_id=schedule_data["schedule_id"],
            arrival_date=datetime.datetime.fromisoformat(schedule_data["arrival_date"]),
            departure_date=datetime.datetime.fromisoformat(schedule_data["departure_date"]),
            route=route
        )

        schedule.schedule_adjustment()  
        controller.add(schedule)
        return {"message": "Horario creado exitosamente"}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except KeyError as ke:
        raise HTTPException(status_code=422, detail=f"Falta el campo: {ke}")
