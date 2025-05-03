from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from backend.app.logic.universal_controller_sql import UniversalController
from backend.app.models.shift import Shift

app = APIRouter(prefix="/shifts", tags=["shifts"])
controller = UniversalController()
templates = Jinja2Templates(directory="src/backend/app/templates")

@app.get("/create", response_class=HTMLResponse)
def crear_turno_form(request: Request):
    return templates.TemplateResponse("CrearTurno.html", {"request": request})

@app.post("/create")
def crear_turno(ID: int = Form(...), TipoTurno: str = Form(...)):
    turno = Shift(ID=ID, TipoTurno=TipoTurno)
    try:
        controller.add(turno)
        return {
            "operation": "create",
            "success": True,
            "data": turno,
            "message": "Turno creado exitosamente."
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/update", response_class=HTMLResponse)
def actualizar_turno_form(request: Request):
    return templates.TemplateResponse("ActualizarTurno.html", {"request": request})

@app.post("/update")
def actualizar_turno(ID: int = Form(...), TipoTurno: str = Form(...)):
    turno = Shift(ID=ID, TipoTurno=TipoTurno)
    try:
        controller.update(turno)
        return {
            "operation": "update",
            "success": True,
            "data": turno,
            "message": "Turno actualizado exitosamente."
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/delete", response_class=HTMLResponse)
def eliminar_turno_form(request: Request):
    return templates.TemplateResponse("EliminarTurno.html", {"request": request})

@app.post("/delete")
def eliminar_turno(ID: int = Form(...)):
    turno = Shift(ID=ID)
    try:
        controller.delete(turno)
        return {
            "operation": "delete",
            "success": True,
            "message": "Turno eliminado exitosamente."
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

"""
from fastapi import APIRouter, Form, HTTPException
from backend.app.logic.universal_controller_sql import UniversalController
from backend.app.models.shift import ShiftCreate

app = APIRouter(prefix="/shifts", tags=["shifts"])
controller = UniversalController()

@app.post("/create")
def crear_turno(
    shift_id: str = Form(...),
    unit_id: str = Form(...),
    start_time: str = Form(...),
    end_time: str = Form(...),
    driver_id: str = Form(...),
    schedule_id: str = Form(...)
):
    turno = ShiftCreate(
        shift_id=shift_id,
        unit_id=unit_id,
        start_time=start_time,
        end_time=end_time,
        driver_id=driver_id,
        schedule_id=schedule_id
    )
    try:
        controller.add(turno)
        return {
            "operation": "create",
            "success": True,
            "data": turno.to_dict(),
            "message": "Turno creado exitosamente."
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/update")
def actualizar_turno(
    shift_id: str = Form(...),
    unit_id: str = Form(...),
    start_time: str = Form(...),
    end_time: str = Form(...),
    driver_id: str = Form(...),
    schedule_id: str = Form(...)
):
    turno = ShiftCreate(
        shift_id=shift_id,
        unit_id=unit_id,
        start_time=start_time,
        end_time=end_time,
        driver_id=driver_id,
        schedule_id=schedule_id
    )
    try:
        controller.update(turno)
        return {
            "operation": "update",
            "success": True,
            "data": turno.to_dict(),
            "message": "Turno actualizado exitosamente."
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.post("/delete")
def eliminar_turno(shift_id: str = Form(...)):
    turno = ShiftCreate(shift_id=shift_id)
    try:
        controller.delete(turno)
        return {
            "operation": "delete",
            "success": True,
            "message": "Turno eliminado exitosamente."
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
"""