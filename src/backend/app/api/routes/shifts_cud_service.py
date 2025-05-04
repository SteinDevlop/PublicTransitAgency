from fastapi import APIRouter, Form, HTTPException, Request, Security
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from backend.app.logic.universal_controller_sql import UniversalController
from backend.app.models.shift import Shift
from backend.app.core.auth import get_current_user  # Import for authentication

app = APIRouter(prefix="/shifts", tags=["shifts"])
controller = UniversalController()
templates = Jinja2Templates(directory="src/backend/app/templates")

@app.get("/create", response_class=HTMLResponse)
def crear_turno_form(
    request: Request,
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "supervisor"])
):
    """
    Render the form for creating a new shift. Requires authentication.
    """
    return templates.TemplateResponse("CrearTurno.html", {"request": request})

@app.post("/create")
def crear_turno(
    ID: int = Form(...),
    TipoTurno: str = Form(...),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "supervisor"])
):
    """
    Create a new shift. Requires authentication.
    """
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
def actualizar_turno_form(
    request: Request,
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "supervisor"])
):
    """
    Render the form for updating a shift. Requires authentication.
    """
    return templates.TemplateResponse("ActualizarTurno.html", {"request": request})

@app.post("/update")
def actualizar_turno(
    ID: int = Form(...),
    TipoTurno: str = Form(...),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "supervisor"])
):
    """
    Update an existing shift. Requires authentication.
    """
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
        raise HTTPException(status_code=404, detail="Turno no encontrado")

@app.get("/delete", response_class=HTMLResponse)
def eliminar_turno_form(
    request: Request,
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "supervisor"])
):
    """
    Render the form for deleting a shift. Requires authentication.
    """
    return templates.TemplateResponse("EliminarTurno.html", {"request": request})

@app.post("/delete")
def eliminar_turno(
    ID: int = Form(...),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "supervisor"])
):
    """
    Delete a shift by ID. Requires authentication.
    """
    turno = Shift(ID=ID)
    try:
        controller.delete(turno)
        return {
            "operation": "delete",
            "success": True,
            "message": "Turno eliminado exitosamente."
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail="Turno no encontrado")
