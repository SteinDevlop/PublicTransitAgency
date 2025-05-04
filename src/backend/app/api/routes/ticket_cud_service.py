from fastapi import APIRouter, Form, HTTPException, Request, Security
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from backend.app.logic.universal_controller_sql import UniversalController
from backend.app.models.ticket import Ticket
from backend.app.core.auth import get_current_user  # Import for authentication

app = APIRouter(prefix="/tickets", tags=["tickets"])
controller = UniversalController()
templates = Jinja2Templates(directory="src/backend/app/templates")

@app.get("/create", response_class=HTMLResponse)  
def crear_ticket_form(
    request: Request,
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "supervisor"])
):
    """
    Render the form for creating a new ticket. Requires authentication.
    """
    return templates.TemplateResponse("CrearTicket.html", {"request": request})

@app.post("/create")
def crear_ticket(
    ticket_id: int = Form(...),
    status_code: int = Form(...),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "supervisor"])
):
    """
    Create a new ticket. Requires authentication.
    """
    ticket = Ticket(ticket_id=ticket_id, status_code=status_code)
    try:
        controller.add(ticket)
        return {
            "operation": "create",
            "success": True,
            "data": ticket,
            "message": "Ticket creado exitosamente."
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/update", response_class=HTMLResponse)
def actualizar_ticket_form(
    request: Request,
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "supervisor"])
):
    """
    Render the form for updating a ticket. Requires authentication.
    """
    return templates.TemplateResponse("ActualizarTicket.html", {"request": request})

@app.post("/update")
def actualizar_ticket(
    ticket_id: int = Form(...),
    status_code: int = Form(...),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "supervisor"])
):
    """
    Update an existing ticket. Requires authentication.
    """
    ticket = Ticket(ticket_id=ticket_id, status_code=status_code)
    try:
        controller.update(ticket)
        return {
            "operation": "update",
            "success": True,
            "data": ticket,
            "message": "Ticket actualizado exitosamente."
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail="Ticket no encontrado")

@app.get("/delete", response_class=HTMLResponse)
def eliminar_ticket_form(
    request: Request,
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "supervisor"])
):
    """
    Render the form for deleting a ticket. Requires authentication.
    """
    return templates.TemplateResponse("EliminarTicket.html", {"request": request})

@app.post("/delete")
def eliminar_ticket(
    ticket_id: int = Form(...),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "supervisor"])
):
    """
    Delete a ticket by ID. Requires authentication.
    """
    ticket = Ticket(ticket_id=ticket_id, status_code=0)
    try:
        controller.delete(ticket)
        return {
            "operation": "delete",
            "success": True,
            "message": "Ticket eliminado exitosamente."
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail="Ticket no encontrado")
