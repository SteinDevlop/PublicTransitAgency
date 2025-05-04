from fastapi import APIRouter, Form, HTTPException, Request, Security
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from backend.app.logic.universal_controller_sql import UniversalController
from backend.app.models.transport import Transport
from backend.app.core.auth import get_current_user  # Import for authentication

app = APIRouter(prefix="/transports", tags=["transports"])
controller = UniversalController()
templates = Jinja2Templates(directory="src/backend/app/templates")

@app.get("/create", response_class=HTMLResponse)
def crear_unidad_form(
    request: Request,
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "supervisor"])
):
    """
    Render the form for creating a new transport unit. Requires authentication.
    """
    return templates.TemplateResponse("CrearTransport.html", {"request": request})

@app.post("/create")
def crear_unidad(
    id: int = Form(...),
    type: str = Form(...),
    status: str = Form(...),
    ubication: str = Form(...),
    capacity: int = Form(...),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "supervisor"])
):
    """
    Create a new transport unit. Requires authentication.
    """
    unidad = Transport(id=id, type=type, status=status, ubication=ubication, capacity=capacity)
    try:
        controller.add(unidad)
        return {
            "operation": "create",
            "success": True,
            "data": unidad,
            "message": "Unidad creada exitosamente."
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/update", response_class=HTMLResponse)
def actualizar_unidad_form(
    request: Request,
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "supervisor"])
):
    """
    Render the form for updating a transport unit. Requires authentication.
    """
    return templates.TemplateResponse("ActualizarTransport.html", {"request": request})

@app.post("/update")
def actualizar_unidad(
    id: int = Form(...),
    type: str = Form(...),
    status: str = Form(...),
    ubication: str = Form(...),
    capacity: int = Form(...),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "supervisor"])
):
    """
    Update an existing transport unit. Requires authentication.
    """
    unidad = Transport(id=id, type=type, status=status, ubication=ubication, capacity=capacity)
    try:
        controller.update(unidad)
        return {
            "operation": "update",
            "success": True,
            "data": unidad,
            "message": "Unidad actualizada exitosamente."
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail="Unidad de transporte no encontrada")

@app.get("/delete", response_class=HTMLResponse)
def eliminar_unidad_form(
    request: Request,
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "supervisor"])
):
    """
    Render the form for deleting a transport unit. Requires authentication.
    """
    return templates.TemplateResponse("EliminarTransport.html", {"request": request})

@app.post("/delete")
def eliminar_unidad(
    id: int = Form(...),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "supervisor"])
):
    """
    Delete a transport unit by ID. Requires authentication.
    """
    unidad = Transport(id=id, type="", status="", ubication="", capacity=0)
    try:
        controller.delete(unidad)
        return {
            "operation": "delete",
            "success": True,
            "message": "Unidad eliminada exitosamente."
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail="Unidad de transporte no encontrada")