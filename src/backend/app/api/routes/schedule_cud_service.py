from fastapi import APIRouter, Form, HTTPException, Request, Security
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from backend.app.logic.universal_controller_postgres import UniversalController
from backend.app.models.schedule import Schedule
from backend.app.core.auth import get_current_user

app = APIRouter(prefix="/schedules", tags=["schedules"])
controller = UniversalController()
templates = Jinja2Templates(directory="src/backend/app/templates")

@app.post("/create")
def crear_horario(
    id: int = Form(...),
    llegada: str = Form(...),
    salida: str = Form(...),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    schedule = Schedule(id=id, llegada=llegada, salida=salida)
    try:
        controller.add(schedule)
        return {"message": "Horario creado exitosamente.", "data": schedule.dict()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/update")
def actualizar_horario(
    id: int = Form(...),
    llegada: str = Form(...),
    salida: str = Form(...),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    schedule = Schedule(id=id, llegada=llegada, salida=salida)
    try:
        controller.update(schedule)
        return {"message": "Horario actualizado exitosamente.", "data": schedule.dict()}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.post("/delete")
def eliminar_horario(
    id: int = Form(...),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    schedule = Schedule(id=id)
    try:
        controller.delete(schedule)
        return {"message": "Horario eliminado exitosamente."}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))