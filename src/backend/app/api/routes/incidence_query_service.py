import logging
from fastapi import APIRouter, HTTPException, Request, Security
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from backend.app.logic.universal_controller_instance import universal_controller as controller

from backend.app.models.incidence import Incidence
from backend.app.core.auth import get_current_user

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

app = APIRouter(prefix="/incidences", tags=["incidences"])
templates = Jinja2Templates(directory="src/backend/app/templates")

@app.get("/", response_class=HTMLResponse)
def listar_incidencias(
    request: Request,
   #current_user: dict = Security(get_current_user, scopes=["system", "administrador", "supervisor"])
):
    """
    Lista todas las incidencias.
    """
    incidencias = controller.read_all(Incidence)
    logger.info(f"[GET /incidences/] Se listaron {len(incidencias)} incidencias.")
    return templates.TemplateResponse("ListarIncidencia.html", {"request": request, "incidencias": incidencias})

@app.get("/{ID}", response_class=HTMLResponse)
def detalle_incidencia(
    ID: int,
    request: Request,
    #current_user: dict = Security(get_current_user, scopes=["system", "administrador", "supervisor"])
):
    """
    Obtiene el detalle de una incidencia por su ID.
    """
    incidencia = controller.get_by_id(Incidence, ID)
    if not incidencia:
        logger.warning(f"[GET /incidences/{ID}] Incidencia no encontrada.")
        raise HTTPException(status_code=404, detail="Incidencia no encontrada.")
    logger.info(f"[GET /incidences/{ID}] Se consultó la incidencia con ID={ID}.")
    return templates.TemplateResponse("DetalleIncidencia.html", {"request": request, "incidencia": incidencia.to_dict()})