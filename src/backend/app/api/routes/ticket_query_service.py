import logging
from fastapi import APIRouter, HTTPException, Security
from fastapi.responses import JSONResponse
from backend.app.logic.universal_controller_instance import universal_controller as controller

from backend.app.models.ticket import Ticket
from backend.app.core.auth import get_current_user
from fastapi import Security

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

app = APIRouter(prefix="/tickets", tags=["tickets"])

@app.get("/", response_class=JSONResponse)
def listar_tickets(
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "operario"])
):
    """
    Lista todos los tickets.
    """
    try:
        tickets = controller.read_all(Ticket)
        logger.info(f"[GET /tickets/] Se listaron {len(tickets)} tickets.")
        tickets_json = [
            t.model_dump() if hasattr(t, "model_dump")
            else t.dict() if hasattr(t, "dict")
            else t
            for t in tickets
        ]
        return tickets_json
    except Exception as e:
        logger.error(f"[GET /tickets/] Error al listar tickets: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/{ID}", response_class=JSONResponse)
def detalle_ticket(
    ID: int,
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "operario"])
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
        if hasattr(ticket, "model_dump"):
            return ticket.model_dump()
        elif hasattr(ticket, "dict"):
            return ticket.dict()
        else:
            return ticket
    except Exception as e:
        logger.error(f"[GET /tickets/{ID}] Error al consultar ticket: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))