import logging
from fastapi import APIRouter, HTTPException, Security
from fastapi.responses import JSONResponse
from backend.app.logic.universal_controller_instance import universal_controller as controller

from backend.app.models.transport import UnidadTransporte
from backend.app.core.auth import get_current_user

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

app = APIRouter(prefix="/transport_units", tags=["transport_units"])

@app.get("/", response_class=JSONResponse)
def listar_unidades_transporte():
    try:
        unidades = controller.read_all(UnidadTransporte)
        logger.info("[GET /transport_units/] Unidades de transporte listadas.")
        unidades_json = [
            u.model_dump() if hasattr(u, "model_dump")
            else u.dict() if hasattr(u, "dict")
            else u
            for u in unidades
        ]
        return unidades_json
    except Exception as e:
        logger.error(f"[GET /transport_units/] Error al listar unidades de transporte: {e}")
        raise HTTPException(status_code=500, detail="Error al listar unidades de transporte.")

@app.get("/{ID}", response_class=JSONResponse)
def detalle_unidad_transporte(ID: str):
    try:
        unidad = controller.get_by_id(UnidadTransporte, ID)
        if not unidad:
            logger.warning(f"[GET /transport_units/{ID}] Unidad de transporte no encontrada.")
            raise HTTPException(status_code=404, detail="Unidad de transporte no encontrada.")
        logger.info("[GET /transport_units/{ID}] Detalle de unidad de transporte consultado.")
        if hasattr(unidad, "model_dump"):
            return unidad.model_dump()
        elif hasattr(unidad, "dict"):
            return unidad.dict()
        else:
            return unidad
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"[GET /transport_units/{ID}] Error al consultar detalle de unidad de transporte: {e}")
        raise HTTPException(status_code=500, detail="Error al consultar detalle de unidad de transporte.")