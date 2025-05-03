from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from backend.app.logic.universal_controller_sql import UniversalController
from backend.app.models.shift import Shift

app = APIRouter(prefix="/shifts", tags=["shifts"])
controller = UniversalController()
templates = Jinja2Templates(directory="src/backend/app/templates")

@app.get("/", response_class=HTMLResponse)
def listar_turnos(request: Request):
    turnos = controller.read_all(Shift)
    return templates.TemplateResponse("ListarTurno.html", {"request": request, "shifts": turnos})

@app.get("/{ID}", response_class=HTMLResponse)
def detalle_turno(ID: int, request: Request):
    turno = controller.get_by_id(Shift, ID)
    if not turno:
        raise HTTPException(status_code=404, detail="Turno no encontrado")
    return templates.TemplateResponse("DetalleTurno.html", {"request": request, "shift": turno})



"""
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from backend.app.logic.universal_controller_sql import UniversalController
from backend.app.models.shift import ShiftOut

app = APIRouter(prefix="/shifts", tags=["shifts"])
controller = UniversalController()

@app.get("/", response_class=JSONResponse)
def listar_turnos():
    shifts = controller.read_all(ShiftOut)
    return [shift.to_dict() for shift in shifts]

@app.get("/{shift_id}", response_class=JSONResponse)
def detalle_turno(shift_id: str):
    turno = controller.get_by_id(ShiftOut, shift_id)
    if not turno:
        raise HTTPException(status_code=404, detail="Turno no encontrado")
    return turno.to_dict()
"""