import logging
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from backend.app.logic.universal_controller_instance import universal_controller as controller

from backend.app.models.stops import Parada

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

app = APIRouter(prefix="/stops", tags=["stops"])

@app.get("/", response_class=JSONResponse)
def listar_paradas():
    """
    Lista todas las paradas.
    """
    try:
        paradas = controller.read_all(Parada)
        logger.info(f"[GET /stops/] Se listaron {len(paradas)} paradas.")
        paradas_json = [
            p.model_dump() if hasattr(p, "model_dump")
            else p.dict() if hasattr(p, "dict")
            else p
            for p in paradas
        ]
        return paradas_json
    except Exception as e:
        logger.error(f"[GET /stops/] Error al listar paradas: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/{id}", response_class=JSONResponse)
def obtener_detalle_parada(id: int):
    """
    Obtiene el detalle de una parada por su ID.
    """
    try:
        parada = controller.get_by_id(Parada, id)
        if not parada:
            logger.warning(f"[GET /stops/{id}] Parada no encontrada.")
            raise HTTPException(status_code=404, detail="Parada no encontrada")
        logger.info(f"[GET /stops/{id}] Se consultó la parada con ID={id}.")
        if hasattr(parada, "model_dump"):
            return parada.model_dump()
        elif hasattr(parada, "dict"):
            return parada.dict()
        else:
            return parada
    except Exception as e:
        logger.error(f"[GET /stops/{id}] Error al consultar parada: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))