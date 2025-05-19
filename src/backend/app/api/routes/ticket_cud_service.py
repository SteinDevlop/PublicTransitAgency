import logging
from fastapi import APIRouter, Form, HTTPException, Security
from backend.app.logic.universal_controller_instance import universal_controller as controller
from backend.app.models.ticket import Ticket
from backend.app.core.auth import get_current_user

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

app = APIRouter(prefix="/tickets", tags=["tickets"])

@app.post("/create")
def crear_ticket(
    ID: int = Form(...),
    EstadoIncidencia: str = Form(...),
    #current_user: dict  = Security(get_current_user, scopes=["system", "administrador"])
):
    """
    Endpoint para crear un ticket.
    """
    ticket = Ticket(ID=ID, EstadoIncidencia=EstadoIncidencia)
    try:
        controller.add(ticket)
        logger.info(f"[POST /tickets/create] Ticket creado exitosamente: {ticket}")
        return {"message": "Ticket creado exitosamente.", "data": ticket.to_dict()}
    except Exception as e:
        logger.warning(f"[POST /tickets/create] Error al crear el ticket: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/update")
def actualizar_ticket(
    ID: int = Form(...),
    EstadoIncidencia: str = Form(...),
    #current_user: dict  = Security(get_current_user, scopes=["system", "administrador"])
):
    """
    Endpoint para actualizar un ticket existente.
    """
    existing_ticket = controller.get_by_id(Ticket, ID)
    if not existing_ticket:
        logger.warning(f"[POST /tickets/update] Ticket no encontrado: ID={ID}")
        raise HTTPException(status_code=404, detail="Ticket no encontrado")

    updated_ticket = Ticket(ID=ID, EstadoIncidencia=EstadoIncidencia)
    try:
        controller.update(updated_ticket)
        logger.info(f"[POST /tickets/update] Ticket actualizado exitosamente: {updated_ticket}")
        return {"message": "Ticket actualizado exitosamente.", "data": updated_ticket.to_dict()}
    except Exception as e:
        logger.warning(f"[POST /tickets/update] Error al actualizar el ticket: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/delete")
def eliminar_ticket(
    ID: int = Form(...),
    #current_user: dict  = Security(get_current_user, scopes=["system", "administrador"])
):
    """
    Endpoint para eliminar un ticket por su ID.
    """
    existing_ticket = controller.get_by_id(Ticket, ID)
    if not existing_ticket:
        logger.warning(f"[POST /tickets/delete] Ticket no encontrado: ID={ID}")
        raise HTTPException(status_code=404, detail="Ticket no encontrado")

    try:
        controller.delete(existing_ticket)
        logger.info(f"[POST /tickets/delete] Ticket eliminado exitosamente: ID={ID}")
        return {"message": "Ticket eliminado exitosamente."}
    except Exception as e:
        logger.warning(f"[POST /tickets/delete] Error al eliminar el ticket: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))