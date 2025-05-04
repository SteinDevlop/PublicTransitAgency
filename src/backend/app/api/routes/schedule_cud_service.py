from fastapi import APIRouter, Form, HTTPException, Request, Security
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from backend.app.logic.universal_controller_sql import UniversalController
from backend.app.models.schedule import Schedule
from backend.app.core.auth import get_current_user  # Import for authentication

app = APIRouter(prefix="/schedules", tags=["schedules"])
controller = UniversalController()
templates = Jinja2Templates(directory="src/backend/app/templates")

@app.get("/create", response_class=HTMLResponse)
def crear_horario_form(
    request: Request,
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "supervisor"])
):
    """
    Render the form for creating a new schedule. Requires authentication.
    """
    return templates.TemplateResponse("CrearHorario.html", {"request": request})

@app.post("/create")
def crear_horario(
    ID: int = Form(...),
    Llegada: str = Form(...),
    Salida: str = Form(...),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "supervisor"])
):
    """
    Create a new schedule. Requires authentication.
    """
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
def actualizar_horario_form(
    request: Request,
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "supervisor"])
):
    """
    Render the form for updating a schedule. Requires authentication.
    """
    return templates.TemplateResponse("ActualizarHorario.html", {"request": request})

@app.post("/update")
def actualizar_horario(
    ID: int = Form(...),
    Llegada: str = Form(...),
    Salida: str = Form(...),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "supervisor"])
):
    """
    Update an existing schedule. Requires authentication.
    """
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
        raise HTTPException(status_code=404, detail="Horario no encontrado")

@app.get("/delete", response_class=HTMLResponse)
def eliminar_horario_form(
    request: Request,
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "supervisor"])
):
    """
    Render the form for deleting a schedule. Requires authentication.
    """
    return templates.TemplateResponse("EliminarHorario.html", {"request": request})

@app.post("/delete")
def eliminar_horario(
    ID: int = Form(...),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "supervisor"])
):
    """
    Delete a schedule by ID. Requires authentication.
    """
    horario = Schedule(ID=ID)
    try:
        controller.delete(horario)
        return {
            "operation": "delete",
            "success": True,
            "message": "Horario eliminado exitosamente."
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail="Horario no encontrado")
