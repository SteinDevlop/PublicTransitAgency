from fastapi import APIRouter, HTTPException, Request, Security
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from backend.app.logic.universal_controller_sql import UniversalController
from backend.app.models.ticket import Ticket
from backend.app.core.auth import get_current_user  # Import for authentication

app = APIRouter(prefix="/tickets", tags=["tickets"])
controller = UniversalController()
templates = Jinja2Templates(directory="src/backend/app/templates")

@app.get("/", response_class=HTMLResponse)
def listar_tickets(
    request: Request,
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "supervisor"])
):
    """
    List all tickets. Requires authentication.
    """
    tickets = controller.read_all(Ticket)
    return templates.TemplateResponse("ListarTickets.html", {"request": request, "tickets": tickets})

@app.get("/{ticket_id}", response_class=HTMLResponse)
def detalle_ticket(
    ticket_id: int,
    request: Request,
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "supervisor"])
):
    """
    Get details of a specific ticket by ID. Requires authentication.
    """
    ticket = controller.get_by_id(Ticket, ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket no encontrado")
    return templates.TemplateResponse("DetalleTicket.html", {"request": request, "ticket": ticket})