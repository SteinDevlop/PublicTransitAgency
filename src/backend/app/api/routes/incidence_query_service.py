import logging
from fastapi import APIRouter, HTTPException, Security
from fastapi.responses import JSONResponse
from backend.app.logic.universal_controller_instance import universal_controller as controller

from backend.app.models.incidence import Incidence
from backend.app.core.auth import get_current_user

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
glob= "Incidencia no encontrada"
app = APIRouter(prefix="/incidences", tags=["incidences"])

@app.get("/", response_class=JSONResponse)
def listar_incidencias(
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
):
    """
    Obtiene el detalle de una incidencia por su ID.
    """
    try:
        incidencia = controller.get_by_id(Incidence, ID)
        if not incidencia:
            logger.warning(f"[GET /incidences/{ID}] {glob}.")
            return JSONResponse(
                status_code=404,
                content={"detail": glob}
            )
        logger.info(f"[GET /incidences/{ID}] Se consultó la incidencia con ID={ID}.")
        if hasattr(incidencia, "model_dump"):
            return JSONResponse(
                status_code=200,
                content={"data": incidencia.model_dump()}
            )
        elif hasattr(incidencia, "dict"):
            return JSONResponse(
                status_code=200,
                content={"data": incidencia.dict()}
            )
        else:
            return JSONResponse(
                status_code=200,
                content={"data": incidencia}
            )
    except Exception as e:
        logger.error(f"[GET /incidences/{ID}] Error interno al consultar incidencia: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"detail": "Error interno al consultar incidencia."}
        )