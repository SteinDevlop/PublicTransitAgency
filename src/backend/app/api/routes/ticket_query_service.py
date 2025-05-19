import logging
from fastapi import APIRouter, HTTPException, Request, Security
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from backend.app.logic.universal_controller_instance import universal_controller as controller

from backend.app.models.ticket import Ticket
from backend.app.core.auth import get_current_user

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

app = APIRouter(prefix="/tickets", tags=["tickets"])
templates = Jinja2Templates(directory="src/backend/app/templates")

@app.get("/", response_class=HTMLResponse)
def listar_tickets(
    request: Request,
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "supervisor"])
):
    """
    Lista todos los tickets.
    """
    try:
        tickets = controller.read_all(Ticket)
        logger.info(f"[GET /tickets/] Se listaron {len(tickets)} tickets.")
        return templates.TemplateResponse("ListarTickets.html", {"request": request, "tickets": tickets})
    except Exception as e:
        logger.error(f"[GET /tickets/] Error al listar tickets: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/{ID}", response_class=HTMLResponse)
def detalle_ticket(
    ID: int,
    request: Request,
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "supervisor"])
):
    """
    Obtiene el detalle de un ticket por su ID.
    """
    try:
        ticket = controller.get_by_id(Ticket, ID)
        if not ticket:
            logger.warning(f"[GET /tickets/{ID}] Ticket no encontrado.")
            raise HTTPException(status_code=404, detail="Ticket no encontrado")
        logger.info(f"[GET /tickets/{ID}] Se consultó el ticket con ID={ID}.")
        return templates.TemplateResponse("DetalleTicket.html", {"request": request, "ticket": ticket.to_dict()})
    except Exception as e:
        logger.error(f"[GET /tickets/{ID}] Error al consultar ticket: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))