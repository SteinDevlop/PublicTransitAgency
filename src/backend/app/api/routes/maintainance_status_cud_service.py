from fastapi import Request, APIRouter, Form, HTTPException, Security
from fastapi.templating import Jinja2Templates
from backend.app.logic.universal_controller_sqlserver import UniversalController
from backend.app.models.maintainance_status import MaintainanceStatus
from backend.app.core.auth import get_current_user
from fastapi.responses import HTMLResponse

app = APIRouter(prefix="/maintainance_status", tags=["maintainance_status"])
controller = UniversalController()
templates = Jinja2Templates(directory="src/backend/app/templates")

@app.get("/create", response_class=HTMLResponse)
def crear_estado_form(
    request: Request,
    current_user: dict = Security(get_current_user, scopes=["system", "mantenimiento"])
):
    """
    Renderiza el formulario para crear un estado de mantenimiento.
    """
    return templates.TemplateResponse("CrearEMantenimiento.html", {"request": request})

@app.get("/update", response_class=HTMLResponse)
def actualizar_estado_form(request: Request):
    return templates.TemplateResponse("ActualizarEMantenimiento.html", {"request": request})

@app.get("/delete", response_class=HTMLResponse)
def eliminar_estado_form(request: Request):
    return templates.TemplateResponse("EliminarEMantenimiento.html", {"request": request})


@app.post("/create")
def crear_estado_mantenimiento(
    ID: str = Form(...),
    TipoEstado: str = Form(...)
):
    """
    Crea un nuevo estado de mantenimiento.
    """
    try:
        nuevo_estado = MaintainanceStatus(ID=ID, TipoEstado=TipoEstado)
        controller.add(nuevo_estado)  # Guarda en la base de datos
        return {"message": "Estado de mantenimiento creado exitosamente."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/update", response_class=HTMLResponse)
def actualizar_estado_form(
    request: Request,
    current_user: dict = Security(get_current_user, scopes=["system", "mantenimiento"])
):
    """
    Renderiza el formulario para actualizar un estado de mantenimiento.
    """
    return templates.TemplateResponse("ActualizarEMantenimiento.html", {"request": request})

@app.post("/update")
def actualizar_estado(
    id: int = Form(...),
    TipoEstado: str = Form(...),
    current_user: dict = Security(get_current_user, scopes=["system", "mantenimiento"])
):
    """
    Actualiza un estado de mantenimiento existente.
    """
    existing_estado = controller.get_by_id(MaintainanceStatus, id)
    if not existing_estado:
        raise HTTPException(status_code=404, detail="Estado de mantenimiento no encontrado")

    estado_actualizado = MaintainanceStatus(ID=id, TipoEstado=TipoEstado)
    try:
        controller.update(estado_actualizado)
        return {"message": "Estado de mantenimiento actualizado exitosamente.", "data": estado_actualizado.to_dict()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/delete", response_class=HTMLResponse)
def eliminar_estado_form(
    request: Request,
    current_user: dict = Security(get_current_user, scopes=["system", "mantenimiento"])
):
    """
    Renderiza el formulario para eliminar un estado de mantenimiento.
    """
    return templates.TemplateResponse("EliminarEMantenimiento.html", {"request": request})

@app.post("/delete")
def eliminar_estado(
    id: int = Form(...),
    current_user: dict = Security(get_current_user, scopes=["system", "mantenimiento"])
):
    """
    Elimina un estado de mantenimiento por su ID.
    """
    existing_estado = controller.get_by_id(MaintainanceStatus, id)
    if not existing_estado:
        raise HTTPException(status_code=404, detail="Estado de mantenimiento no encontrado")

    try:
        controller.delete(existing_estado)
        return {"message": "Estado de mantenimiento eliminado exitosamente."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
