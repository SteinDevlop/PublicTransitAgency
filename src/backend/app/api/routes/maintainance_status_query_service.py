import logging
from fastapi import APIRouter, HTTPException, Request, Security
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from backend.app.logic.universal_controller_instance import universal_controller as controller
from backend.app.models.maintainance_status import MaintainanceStatus
from backend.app.core.auth import get_current_user

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

app = APIRouter(prefix="/maintainance_status", tags=["maintainance_status"])
templates = Jinja2Templates(directory="src/backend/app/templates")

@app.get("/", response_class=HTMLResponse)
def listar_estados(
    request: Request,
    ##current_user: dict = Security(get_current_user, scopes=["system", "mantenimiento"])
):
    """
    Lista todos los estados de mantenimiento.
    """
    try:
        estados = controller.read_all(MaintainanceStatus)
        logger.info(f"[GET /maintainance_status/] Se listaron {len(estados)} estados de mantenimiento.")
        return templates.TemplateResponse("ListaEstados.html", {"request": request, "estados": estados})
    except Exception as e:
        logger.error(f"[GET /maintainance_status/] Error al listar estados: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/{id:int}", response_class=HTMLResponse)
def detalle_estado(
    id: int,
    request: Request,
    ##current_user: dict = Security(get_current_user, scopes=["system", "mantenimiento"])
):
    """
    Obtiene el detalle de un estado de mantenimiento por su ID.
    """
    try:
        estado = controller.get_by_id(MaintainanceStatus, id)
        if not estado:
            logger.warning(f"[GET /maintainance_status/{id}] Estado de mantenimiento no encontrado.")
            raise HTTPException(status_code=404, detail="Estado de mantenimiento no encontrado")
        logger.info(f"[GET /maintainance_status/{id}] Se consultó el estado de mantenimiento con ID={id}.")
        return templates.TemplateResponse("DetalleEMantenimiento.html", {"request": request, "estado": estado.to_dict()})
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"[GET /maintainance_status/{id}] Error al consultar estado: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))