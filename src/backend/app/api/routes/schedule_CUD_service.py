from fastapi import FastAPI, Form, HTTPException, APIRouter, Request
import datetime
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from backend.app.models.schedule import ScheduleCreate, ScheduleOut
from backend.app.logic.universal_controller_sql import UniversalController

app = APIRouter(prefix="/schedules", tags=["schedules"])
controller = UniversalController()
templates = Jinja2Templates(directory="src/backend/app/templates")

@app.get("/crear", response_class=HTMLResponse)
def index_create(request: Request):
    return templates.TemplateResponse("CrearHorario.html", {"request": request})

@app.get("/actualizar", response_class=HTMLResponse)
def index_update(request: Request):
    return templates.TemplateResponse("ActualizarHorario.html", {"request": request})

@app.get("/eliminar", response_class=HTMLResponse)
def index_delete(request: Request):
    return templates.TemplateResponse("EliminarHorario.html", {"request": request})

@app.post("/create")
async def create_schedule(
    schedule_id: str = Form(...),
    arrival_date: datetime.datetime = Form(...),
    departure_date: datetime.datetime = Form(...),
    route_id: str = Form(...)
):
    try:
        new_schedule = ScheduleCreate(
            schedule_id=schedule_id,
            arrival_date=arrival_date,
            departure_date=departure_date,
            route_id=route_id
        )
        result = controller.add(new_schedule)
        return {"operation": "create", "success": True, "data": ScheduleOut(**result.to_dict()).dict(), "message": "Schedule created successfully"}
    except ValueError as e:
        raise HTTPException(400, detail=str(e))
    except Exception as e:
        raise HTTPException(500, detail=f"Internal server error: {str(e)}")

@app.post("/update/{schedule_id}")
async def update_schedule(
    schedule_id: str,
    arrival_date: datetime.datetime = Form(None),
    departure_date: datetime.datetime = Form(None),
    route_id: str = Form(None)
):
    try:
        existing_schedule = controller.get_by_id(ScheduleOut, schedule_id)
        if not existing_schedule:
            raise HTTPException(404, detail="Schedule not found")

        update_data = ScheduleCreate(
            schedule_id=schedule_id,  # ID from path, ensure consistency
            arrival_date=arrival_date if arrival_date is not None else existing_schedule.arrival_date,
            departure_date=departure_date if departure_date is not None else existing_schedule.departure_date,
            route_id=route_id if route_id is not None else existing_schedule.route_id
        )
        result = controller.update(update_data)
        return {"operation": "update", "success": True, "data": ScheduleOut(**result.to_dict()).dict(), "message": f"Schedule {schedule_id} updated successfully"}
    except ValueError as e:
        raise HTTPException(400, detail=str(e))
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(500, detail=str(e))

@app.post("/delete/{schedule_id}")
async def delete_schedule(schedule_id: str):
    try:
        existing_schedule = controller.get_by_id(ScheduleOut, schedule_id)
        if not existing_schedule:
            raise HTTPException(404, detail="Schedule not found")
        controller.delete(existing_schedule)
        return {"operation": "delete", "success": True, "message": f"Schedule {schedule_id} deleted successfully"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(500, detail=str(e))