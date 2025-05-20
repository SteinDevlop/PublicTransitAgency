import logging
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from backend.app.logic.universal_controller_instance import universal_controller as controller

from backend.app.models.stops import Parada

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

app = APIRouter(prefix="/stops", tags=["stops"])
templates = Jinja2Templates(directory="src/backend/app/templates")

@app.get("/", response_class=HTMLResponse)
def listar_paradas(
    request: Request,
):
    """
    Lista todas las paradas.
    """
    try:
        paradas = controller.read_all(Parada)
        logger.info(f"[GET /stops/] Se listaron {len(paradas)} paradas.")
        return templates.TemplateResponse("ListarParadas.html", {"request": request, "paradas": paradas})
    except Exception as e:
        logger.error(f"[GET /stops/] Error al listar paradas: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/{id}", response_class=HTMLResponse)
def obtener_detalle_parada(
    id: int,
    request: Request,
):
    """
    Obtiene el detalle de una parada por su ID.
    """
    try:
        parada = controller.get_by_id(Parada, id)
        if not parada:
            logger.warning(f"[GET /stops/{id}] Parada no encontrada.")
            raise HTTPException(status_code=404, detail="Parada no encontrada")
        logger.info(f"[GET /stops/{id}] Se consultó la parada con ID={id}.")
        return templates.TemplateResponse("DetalleParada.html", {"request": request, "parada": parada.to_dict()})
    except Exception as e:
        logger.error(f"[GET /stops/{id}] Error al consultar parada: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))