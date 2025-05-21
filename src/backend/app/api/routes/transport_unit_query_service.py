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
):
    try:
        unidades = controller.read_all(UnidadTransporte)
        logger.info("[GET /transport_units/] Unidades de transporte listadas.")
        return templates.TemplateResponse(request, "ListarTransports.html", {"unidades": unidades})
    except Exception as e:
        logger.error(f"[GET /transport_units/] Error al listar unidades de transporte: {e}")
        raise HTTPException(status_code=500, detail="Error al listar unidades de transporte.")

@app.get("/{ID}", response_class=HTMLResponse)
def detalle_unidad_transporte(
    ID: str,
    request: Request,
):
    try:
        unidad = controller.get_by_id(UnidadTransporte, ID)
        if not unidad:
            logger.warning(f"[GET /transport_units/{ID}] Unidad de transporte no encontrada.")
            raise HTTPException(status_code=404, detail="Unidad de transporte no encontrada.")
        logger.info("[GET /transport_units/{ID}] Detalle de unidad de transporte consultado.")
        return templates.TemplateResponse(request, "DetalleTransport.html", {"unidad": unidad})
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"[GET /transport_units/{ID}] Error al consultar detalle de unidad de transporte: {e}")
        raise HTTPException(status_code=500, detail="Error al consultar detalle de unidad de transporte.")