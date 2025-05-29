import logging
from fastapi import APIRouter, Form, HTTPException, Security
from fastapi.responses import JSONResponse
from backend.app.logic.universal_controller_instance import universal_controller as controller
from backend.app.models.ticket import Ticket
# from backend.app.core.auth import get_current_user  # Comentado para inutilizar autenticación temporalmente
# from backend.app.core.conf import headers  # Comentado para inutilizar autenticación temporalmente

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

TICKET_NO_ENCONTRADO = "Ticket no encontrado."
ERROR_AL_CREAR = "Error al crear el ticket."
ERROR_AL_ACTUALIZAR = "Error al actualizar el ticket."
ERROR_AL_ELIMINAR = "Error al eliminar el ticket."

app = APIRouter(prefix="/tickets", tags=["tickets"])

@app.post("/create")
def crear_ticket(
    ID: int = Form(...),
    EstadoIncidencia: str = Form(...),
    # current_user: dict = Security(get_current_user, scopes=["system"])  # Comentado para inutilizar autenticación temporalmente
):
    """
    Crea un nuevo ticket.
    """
    new_ticket = Ticket(ID=ID, EstadoIncidencia=EstadoIncidencia)
    try:
        controller.add(new_ticket)
        logger.info(f"[POST /tickets/create] Ticket creado exitosamente: {new_ticket}")
        return {"message": "Ticket creado exitosamente.", "data": new_ticket.to_dict()}
    except Exception as e:
        logger.warning(f"[POST /tickets/create] {ERROR_AL_CREAR}: {str(e)}")
        return JSONResponse(
            status_code=400,
            content={"detail": ERROR_AL_CREAR}
        )

@app.post("/update")
def actualizar_ticket(
    ID: int = Form(...),
    EstadoIncidencia: str = Form(...),
    # current_user: dict = Security(get_current_user, scopes=["system"])  # Comentado para inutilizar autenticación temporalmente
):
    try:
        existing_ticket = controller.get_by_id(Ticket, ID)
        if not existing_ticket:
            logger.warning(f"[POST /tickets/update] {TICKET_NO_ENCONTRADO}: ID={ID}")
            return JSONResponse(
                status_code=404,
                content={"detail": TICKET_NO_ENCONTRADO}
            )
        updated_ticket = Ticket(ID=ID, EstadoIncidencia=EstadoIncidencia)
        controller.update(updated_ticket)
        logger.info(f"[POST /tickets/update] Ticket actualizado exitosamente: {updated_ticket}")
        return {"message": "Ticket actualizado exitosamente.", "data": updated_ticket.to_dict()}
    except Exception as e:
        logger.warning(f"[POST /tickets/update] {ERROR_AL_ACTUALIZAR}: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"detail": ERROR_AL_ACTUALIZAR}
        )

@app.post("/delete")
def eliminar_ticket(
    ID: int = Form(...),
    # current_user: dict = Security(get_current_user, scopes=["system"])  # Comentado para inutilizar autenticación temporalmente
):
    try:
        existing_ticket = controller.get_by_id(Ticket, ID)
        if not existing_ticket:
            logger.warning(f"[POST /tickets/delete] {TICKET_NO_ENCONTRADO}: ID={ID}")
            return JSONResponse(
                status_code=404,
                content={"detail": TICKET_NO_ENCONTRADO}
            )
        controller.delete(existing_ticket)
        logger.info(f"[POST /tickets/delete] Ticket eliminado exitosamente: ID={ID}")
        return {"message": "Ticket eliminado exitosamente."}
    except Exception as e:
        logger.warning(f"[POST /tickets/delete] {ERROR_AL_ELIMINAR}: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"detail": ERROR_AL_ELIMINAR}
        )