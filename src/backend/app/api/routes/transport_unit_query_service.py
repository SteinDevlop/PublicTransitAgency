import logging
from fastapi import APIRouter, HTTPException  # Se mantiene la importación de Security para uso futuro
from fastapi.responses import JSONResponse
from backend.app.logic.universal_controller_instance import universal_controller as controller
from backend.app.models.transport import UnidadTransporte
# from backend.app.core.auth import get_current_user  # Comentado para pruebas

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

app = APIRouter(prefix="/transport_units", tags=["transport_units"])

@app.get("/", response_class=JSONResponse)
def listar_unidades_transporte():  # current_user: dict = Security(get_current_user)  # Comentado para pruebas
    """
    Lista todas las unidades de transporte.
    """
    try:
        unidades = controller.read_all(UnidadTransporte)
        logger.info("[GET /transport_units/] Unidades de transporte listadas.")
        unidades_json = [
            u.model_dump() if hasattr(u, "model_dump")
            else u.dict() if hasattr(u, "dict")
            else u
            for u in unidades
        ]
        return {"data": unidades_json}
    except Exception as e:
        logger.error("[GET /transport_units/] Error al listar unidades de transporte: %s", e)
        return JSONResponse(
            status_code=500,
            content={"detail": "Error al listar unidades de transporte."}
        )

@app.get("/{ID}", response_class=JSONResponse)
def detalle_unidad_transporte(ID: str):  # current_user: dict = Security(get_current_user)  # Comentado para pruebas
    """
    Obtiene el detalle de una unidad de transporte por su ID.
    """
    try:
        unidad = controller.get_by_id(UnidadTransporte, ID)
        if not unidad:
            logger.warning("[GET /transport_units/{ID}] Unidad de transporte no encontrada: ID=%s", ID)
            return JSONResponse(
                status_code=404,
                content={"detail": "Unidad de transporte no encontrada."}
            )
        logger.info("[GET /transport_units/{ID}] Detalle de unidad de transporte consultado: ID=%s", ID)
        if hasattr(unidad, "model_dump"):
            return {"data": unidad.model_dump()}
        elif hasattr(unidad, "dict"):
            return {"data": unidad.dict()}
        else:
            return {"data": unidad}
    except Exception as e:
        logger.error("[GET /transport_units/{ID}] Error al consultar detalle de unidad de transporte: %s", e)
        return JSONResponse(
            status_code=500,
            content={"detail": "Error al consultar detalle de unidad de transporte."}
        )