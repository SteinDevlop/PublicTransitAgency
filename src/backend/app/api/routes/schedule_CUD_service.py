from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from backend.app.logic.universal_controller_sql import UniversalController
from backend.app.models.schedule import Schedule

app = APIRouter(prefix="/schedules", tags=["schedules"])
controller = UniversalController()
templates = Jinja2Templates(directory="src/backend/app/templates")

@app.get("/create", response_class=HTMLResponse)
def crear_horario_form(request: Request):
    return templates.TemplateResponse("CrearHorario.html", {"request": request})

@app.post("/create")
def crear_horario(ID: int = Form(...), Llegada: str = Form(...), Salida: str = Form(...)):
    horario = Schedule(ID=ID, Llegada=Llegada, Salida=Salida)
    try:
        controller.add(horario)
        return {
            "operation": "create",
            "success": True,
            "data": horario,
            "message": "Horario creado exitosamente."
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/update", response_class=HTMLResponse)
def actualizar_horario_form(request: Request):
    return templates.TemplateResponse("ActualizarHorario.html", {"request": request})

@app.post("/update")
def actualizar_horario(ID: int = Form(...), Llegada: str = Form(...), Salida: str = Form(...)):
    horario = Schedule(ID=ID, Llegada=Llegada, Salida=Salida)
    try:
        controller.update(horario)
        return {
            "operation": "update",
            "success": True,
            "data": horario,
            "message": "Horario actualizado exitosamente."
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/delete", response_class=HTMLResponse)
def eliminar_horario_form(request: Request):
    return templates.TemplateResponse("EliminarHorario.html", {"request": request})

@app.post("/delete")
def eliminar_horario(ID: int = Form(...)):
    horario = Schedule(ID=ID)
    try:
        controller.delete(horario)
        return {
            "operation": "delete",
            "success": True,
            "message": "Horario eliminado exitosamente."
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))