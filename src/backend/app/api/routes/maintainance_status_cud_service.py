from fastapi import APIRouter, Form, HTTPException, Security
from fastapi.templating import Jinja2Templates
from backend.app.logic.universal_controller_postgres import UniversalController
from backend.app.models.maintainance_status import MaintainanceState
from backend.app.core.auth import get_current_user

app = APIRouter(prefix="/maintainance_state", tags=["maintainance_state"])
controller = UniversalController()
templates = Jinja2Templates(directory="src/backend/app/templates")

@app.post("/create")
def crear_estado(
    id: int = Form(...),
    tipoestado: str = Form(...),
    current_user: dict = Security(get_current_user, scopes=["system", "mantenimiento"])
):
    estado = MaintainanceState(id=id, tipoestado=tipoestado)
    try:
        controller.add(estado)
        return {
            "message": "Estado de mantenimiento creado exitosamente.",
            "data": estado.dict()
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/update")
def actualizar_estado(
    id: int = Form(...),
    tipoestado: str = Form(...),
    current_user: dict = Security(get_current_user, scopes=["system", "mantenimiento"])
):
    estado = MaintainanceState(id=id, tipoestado=tipoestado)
    try:
        controller.update(estado)
        return {
            "message": "Estado de mantenimiento actualizado exitosamente.",
            "data": estado.dict()
        }
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.post("/delete")
def eliminar_estado(
    id: int = Form(...),
    current_user: dict = Security(get_current_user, scopes=["system", "mantenimiento"])
):
    estado = MaintainanceState(id=id, tipoestado="")
    try:
        controller.delete(estado)
        return {"message": "Estado de mantenimiento eliminado exitosamente."}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))