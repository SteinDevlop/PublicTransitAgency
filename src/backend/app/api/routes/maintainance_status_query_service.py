import logging
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from backend.app.logic.universal_controller_instance import universal_controller as controller
from backend.app.models.maintainance_status import MaintainanceStatus
from backend.app.core.auth import get_current_active_user

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

app = APIRouter(prefix="/maintainance_status", tags=["maintainance_status"])

@app.get("/", response_class=JSONResponse)
def listar_estados(
     current_user: dict = Depends(get_current_active_user)
):
    """
    Lista todos los estados de mantenimiento.
    """
    try:
        estados = controller.read_all(MaintainanceStatus)
        logger.info(f"[GET /maintainance_status/] Se listaron {len(estados)} estados de mantenimiento.")
        estados_json = [
            e.model_dump() if hasattr(e, "model_dump")
            else e.dict() if hasattr(e, "dict")
            else e
            for e in estados
        ]
        return JSONResponse(status_code=200, content={"data": estados_json})
    except Exception as e:
        logger.error(f"[GET /maintainance_status/] Error al listar estados: {str(e)}")
        return JSONResponse(status_code=500, content={"detail": str(e)})

@app.get("/{id:int}", response_class=JSONResponse)
def detalle_estado(
    id: int,
    # current_user: dict = Depends(get_current_active_user)
):
    """
    Obtiene el detalle de un estado de mantenimiento por su ID.
    """
    try:
        estado = controller.get_by_id(MaintainanceStatus, id)
        if not estado:
            logger.warning(f"[GET /maintainance_status/{id}] Estado de mantenimiento no encontrado.")
            return JSONResponse(status_code=404, content={"detail": "Estado de mantenimiento no encontrado"})
        logger.info(f"[GET /maintainance_status/{id}] Se consultó el estado de mantenimiento con ID={id}.")
        if hasattr(estado, "model_dump"):
            return JSONResponse(status_code=200, content={"data": estado.model_dump()})
        elif hasattr(estado, "dict"):
            return JSONResponse(status_code=200, content={"data": estado.dict()})
        else:
            return JSONResponse(status_code=200, content={"data": estado})
    except Exception as e:
        logger.error(f"[GET /maintainance_status/{id}] Error al consultar estado: {str(e)}")
        return JSONResponse(status_code=500, content={"detail": str(e)})