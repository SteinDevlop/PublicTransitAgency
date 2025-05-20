import logging
from fastapi import APIRouter, HTTPException, Request, Security
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from backend.app.logic.universal_controller_instance import universal_controller as controller

from backend.app.models.transport import UnidadTransporte
from backend.app.core.auth import get_current_user

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

app = APIRouter(prefix="/transport_units", tags=["transport_units"])
templates = Jinja2Templates(directory="src/backend/app/templates")

@app.get("/", response_class=HTMLResponse)
def listar_unidades_transporte(
    request: Request,
   #current_user: dict  = Security(get_current_user, scopes=["system", "administrador", "supervisor", "operador"])
):
    """
    Lista todas las unidades de transporte.
    """
    try:
        unidades = controller.read_all(UnidadTransporte)
        logger.info(f"[GET /transport_units/] Se listaron {len(unidades)} unidades de transporte.")
        return templates.TemplateResponse("ListarTransports.html", {"request": request, "unidades": unidades})
    except Exception as e:
        logger.error(f"[GET /transport_units/] Error al listar unidades: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/{ID}", response_class=HTMLResponse)
def detalle_unidad_transporte(
    ID: str,
    request: Request,
   #current_user: dict  = Security(get_current_user, scopes=["system", "administrador", "supervisor", "operador"])
):
    """
    Obtiene el detalle de una unidad de transporte por su ID.
    """
    try:
        unidad = controller.get_by_id(UnidadTransporte, ID)
        if not unidad:
            logger.warning(f"[GET /transport_units/{ID}] Unidad de transporte no encontrada.")
            raise HTTPException(status_code=404, detail="Unidad de transporte no encontrada.")
        logger.info(f"[GET /transport_units/{ID}] Se consultó la unidad con ID={ID}.")
        return templates.TemplateResponse("DetalleTransport.html", {"request": request, "unidad": unidad.to_dict()})
    except Exception as e:
        logger.error(f"[GET /transport_units/{ID}] Error al consultar unidad: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))