from fastapi import FastAPI, APIRouter, Request, Query
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi import HTTPException
from fastapi.templating import Jinja2Templates
from typing import List

from backend.app.models.schedule import ScheduleOut
from backend.app.logic.universal_controller_sql import UniversalController

app = APIRouter(prefix="/schedules", tags=["schedules"])
controller = UniversalController()
templates = Jinja2Templates(directory="src/backend/app/templates")

@app.get("/listar", response_class=HTMLResponse)
def list_schedules_page(request: Request):
    schedules = controller.read_all(ScheduleOut)
    return templates.TemplateResponse("ListarHorario.html", {"request": request, "schedules": schedules})

@app.get("/detalles/{schedule_id}", response_class=HTMLResponse)
def schedule_detail_page(request: Request, schedule_id: str):
    schedule = controller.get_by_id(ScheduleOut, schedule_id)
    if not schedule:
        raise HTTPException(404, detail="Schedule not found")
    return templates.TemplateResponse("DetalleHorario.html", {"request": request, "schedule": schedule})

@app.get("/all")
async def get_all_schedules():
    return controller.read_all(ScheduleOut)

@app.get("/{schedule_id}")
async def get_schedule_by_id(schedule_id: str):
    schedule = controller.get_by_id(ScheduleOut, schedule_id)
    if schedule:
        return schedule
    raise HTTPException(404, detail="Schedule not found")