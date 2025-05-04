from fastapi import APIRouter, Form, HTTPException, Request, Security
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from backend.app.logic.universal_controller_sql import UniversalController
from backend.app.models.stops import Stop
from backend.app.core.auth import get_current_user  # Import for authentication

app = APIRouter(prefix="/stops", tags=["stops"])
controller = UniversalController()
templates = Jinja2Templates(directory="src/backend/app/templates")

@app.get("/create", response_class=HTMLResponse)
def crear_parada_form(
    request: Request,
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "supervisor"])
):
    """
    Render the form for creating a new stop. Requires authentication.
    """
    return templates.TemplateResponse("CrearParada.html", {"request": request})

@app.post("/create")
def crear_parada(
    ID: int = Form(...),
    Nombre: str = Form(...),
    Ubicacion: str = Form(...),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "supervisor"])
):
    """
    Create a new stop. Requires authentication.
    """
    parada = Stop(ID=ID, Nombre=Nombre, Ubicacion=Ubicacion)
    try:
        controller.add(parada)
        return {
            "operation": "create",
            "success": True,
            "data": parada,
            "message": "Parada creada exitosamente."
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/update", response_class=HTMLResponse)
def actualizar_parada_form(
    request: Request,
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "supervisor"])
):
    """
    Render the form for updating a stop. Requires authentication.
    """
    return templates.TemplateResponse("ActualizarParada.html", {"request": request})

@app.post("/update")
def actualizar_parada(
    ID: int = Form(...),
    Nombre: str = Form(...),
    Ubicacion: str = Form(...),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "supervisor"])
):
    """
    Update an existing stop. Requires authentication.
    """
    parada = Stop(ID=ID, Nombre=Nombre, Ubicacion=Ubicacion)
    try:
        controller.update(parada)
        return {
            "operation": "update",
            "success": True,
            "data": parada,
            "message": "Parada actualizada exitosamente."
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail="Parada no encontrada")

@app.get("/delete", response_class=HTMLResponse)
def eliminar_parada_form(
    request: Request,
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "supervisor"])
):
    """
    Render the form for deleting a stop. Requires authentication.
    """
    return templates.TemplateResponse("EliminarParada.html", {"request": request})

@app.post("/delete")
def eliminar_parada(
    ID: int = Form(...),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "supervisor"])
):
    """
    Delete a stop by ID. Requires authentication.
    """
    parada = Stop(ID=ID)
    try:
        controller.delete(parada)
        return {
            "operation": "delete",
            "success": True,
            "message": "Parada eliminada exitosamente."
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail="Parada no encontrada")
