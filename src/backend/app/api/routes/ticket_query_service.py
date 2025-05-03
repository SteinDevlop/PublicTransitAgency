from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from backend.app.logic.universal_controller_sql import UniversalController
from backend.app.models.ticket import Ticket

app = APIRouter(prefix="/tickets", tags=["tickets"])
controller = UniversalController()
templates = Jinja2Templates(directory="src/backend/app/templates")

@app.get("/", response_class=HTMLResponse)
def listar_tickets(request: Request):
    tickets = controller.read_all(Ticket)
    return templates.TemplateResponse("ListarTickets.html", {"request": request, "tickets": tickets})

@app.get("/{ticket_id}", response_class=HTMLResponse)
def detalle_ticket(ticket_id: int, request: Request):
    ticket = controller.get_by_id(Ticket, ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket no encontrado")
    return templates.TemplateResponse("DetalleTicket.html", {"request": request, "ticket": ticket})