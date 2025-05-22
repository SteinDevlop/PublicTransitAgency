import logging
from fastapi import APIRouter, HTTPException, Security
from fastapi.responses import JSONResponse
from backend.app.logic.universal_controller_instance import universal_controller as controller

from backend.app.models.incidence import Incidence
from backend.app.core.auth import get_current_user

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

app = APIRouter(prefix="/incidences", tags=["incidences"])

@app.get("/", response_class=JSONResponse)
def listar_incidencias(
    #current_user: dict = Security(get_current_user, scopes=["system", "administrador", "supervisor"])
):
    """
    Lista todas las incidencias.
    """
    incidencias = controller.read_all(Incidence)
    logger.info(f"[GET /incidences/] Se listaron {len(incidencias)} incidencias.")
    incidencias_json = [
        i.model_dump() if hasattr(i, "model_dump")
        else i.dict() if hasattr(i, "dict")
        else i
        for i in incidencias
    ]
    return incidencias_json

@app.get("/{ID}", response_class=JSONResponse)
def detalle_incidencia(
    ID: int,
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
    if hasattr(incidencia, "model_dump"):
        return incidencia.model_dump()
    elif hasattr(incidencia, "dict"):
        return incidencia.dict()
    else:
        return incidencia