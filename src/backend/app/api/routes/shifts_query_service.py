

from fastapi import FastAPI, APIRouter, Request, Query
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi import HTTPException
from fastapi.templating import Jinja2Templates
from typing import List

from backend.app.models.shift import ShiftOut
from backend.app.logic.universal_controller_sql import UniversalController

app = APIRouter(prefix="/shifts", tags=["shifts"])
controller = UniversalController()
templates = Jinja2Templates(directory="src/backend/app/templates")

@app.get("/listar", response_class=HTMLResponse)
def list_shifts_page(request: Request):
    shifts = controller.read_all(ShiftOut)
    return templates.TemplateResponse("ListarTurno.html", {"request": request, "shifts": shifts})

@app.get("/detalles/{shift_id}", response_class=HTMLResponse)
def shift_detail_page(request: Request, shift_id: str):
    shift = controller.get_by_id(ShiftOut, shift_id)
    if not shift:
        raise HTTPException(404, detail="Shift not found")
    return templates.TemplateResponse("DetalleTurno.html", {"request": request, "shift": shift})

@app.get("/all")
async def get_all_shifts():
    return controller.read_all(ShiftOut)

@app.get("/{shift_id}")
async def get_shift_by_id(shift_id: str):
    shift = controller.get_by_id(ShiftOut, shift_id)
    if shift:
        return shift
    raise HTTPException(404, detail="Shift not found")