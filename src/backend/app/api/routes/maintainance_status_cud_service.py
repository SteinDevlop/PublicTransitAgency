from fastapi import APIRouter, Form, HTTPException, Request, Security
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from backend.app.logic.universal_controller_sql import UniversalController
from backend.app.models.maintainance_status import MaintainanceStatus
from backend.app.core.auth import get_current_user  # Import for authentication

app = APIRouter(prefix="/maintainance_status", tags=["maintainance_status"])
controller = UniversalController()
templates = Jinja2Templates(directory="src/backend/app/templates")

@app.get("/create", response_class=HTMLResponse)
def crear_estado_form(
    request: Request,
    current_user: dict = Security(get_current_user, scopes=["system", "mantenimiento"])
):
    """
    Render the form for creating a new maintenance status. Requires authentication.
    """
    return templates.TemplateResponse("CrearEMantenimiento.html", {"request": request})

@app.post("/create")
def crear_estado(
    id: int = Form(...),
    unit: str = Form(...),
    type: str = Form(...),
    status: str = Form(...),
    current_user: dict = Security(get_current_user, scopes=["system", "mantenimiento"])
):
    """
    Create a new maintenance status. Requires authentication.
    """
    estado = MaintainanceStatus(id=id, unit=unit, type=type, status=status)
    try:
        controller.add(estado)
        return {
            "operation": "create",
            "success": True,
            "data": estado,
            "message": "Estado de mantenimiento creado exitosamente."
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/update", response_class=HTMLResponse)
def actualizar_estado_form(
    request: Request,
    current_user: dict = Security(get_current_user, scopes=["system", "mantenimiento"])
):
    """
    Render the form for updating a maintenance status. Requires authentication.
    """
    return templates.TemplateResponse("ActualizarEMantenimiento.html", {"request": request})

@app.post("/update")
def actualizar_estado(
    id: int = Form(...),
    unit: str = Form(...),
    type: str = Form(...),
    status: str = Form(...),
    current_user: dict = Security(get_current_user, scopes=["system", "mantenimiento"])
):
    """
    Update an existing maintenance status. Requires authentication.
    """
    estado = MaintainanceStatus(id=id, unit=unit, type=type, status=status)
    try:
        controller.update(estado)
        return {
            "operation": "update",
            "success": True,
            "data": estado,
            "message": "Estado de mantenimiento actualizado exitosamente."
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail="Estado de mantenimiento no encontrado")

@app.get("/delete", response_class=HTMLResponse)
def eliminar_estado_form(
    request: Request,
    current_user: dict = Security(get_current_user, scopes=["system", "mantenimiento"])
):
    """
    Render the form for deleting a maintenance status. Requires authentication.
    """
    return templates.TemplateResponse("EliminarEMantenimiento.html", {"request": request})

@app.post("/delete")
def eliminar_estado(
    id: int = Form(...),
    current_user: dict = Security(get_current_user, scopes=["system", "mantenimiento"])
):
    """
    Delete a maintenance status by ID. Requires authentication.
    """
    estado = MaintainanceStatus(id=id)
    try:
        controller.delete(estado)
        return {
            "operation": "delete",
            "success": True,
            "message": "Estado de mantenimiento eliminado exitosamente."
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail="Estado de mantenimiento no encontrado")
