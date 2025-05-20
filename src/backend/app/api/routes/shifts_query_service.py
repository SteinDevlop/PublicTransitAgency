import logging
from fastapi import APIRouter, HTTPException, Request, Security
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from backend.app.logic.universal_controller_instance import universal_controller as controller

from backend.app.models.shift import Shift
from backend.app.core.auth import get_current_user

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

app = APIRouter(prefix="/shifts", tags=["shifts"])
templates = Jinja2Templates(directory="src/backend/app/templates")

@app.get("/", response_class=HTMLResponse)
def listar_turnos(
    request: Request,
   #current_user: dict  = Security(get_current_user, scopes=["system", "administrador", "supervisor"])
):
    """
    Consulta la lista de todos los turnos.
    """
    try:
        turnos = controller.read_all(Shift)
        logger.info(f"[GET /shifts/] Se listaron {len(turnos)} turnos.")
        return templates.TemplateResponse("ListarTurno.html", {"request": request, "turnos": turnos})
    except Exception as e:
        logger.error(f"[GET /shifts/] Error al listar turnos: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/{id}", response_class=HTMLResponse)
def detalle_turno(
    id: int,
    request: Request,
   #current_user: dict  = Security(get_current_user, scopes=["system", "administrador", "supervisor"])
):
    """
    Consulta el detalle de un turno en específico por su ID.
    """
    try:
        turno = controller.get_by_id(Shift, id)
        if not turno:
            logger.warning(f"[GET /shifts/{id}] Turno no encontrado.")
            raise HTTPException(status_code=404, detail="Turno no encontrado")
        logger.info(f"[GET /shifts/{id}] Se consultó el turno con ID={id}.")
        return templates.TemplateResponse("DetalleTurno.html", {"request": request, "turno": turno.to_dict()})
    except Exception as e:
        logger.error(f"[GET /shifts/{id}] Error al consultar turno: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))