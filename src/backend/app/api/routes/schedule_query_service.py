import logging
from fastapi import APIRouter, HTTPException, Security
from fastapi.responses import JSONResponse
from backend.app.logic.universal_controller_instance import universal_controller as controller

from backend.app.models.schedule import Schedule
from backend.app.core.auth import get_current_user

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

app = APIRouter(prefix="/schedules", tags=["schedules"])

@app.get("/", response_class=JSONResponse)
def listar_horarios():
    """
    Lista todos los horarios.
    """
    try:
        horarios = controller.read_all(Schedule)
        logger.info(f"[GET /schedules/] Se listaron {len(horarios)} horarios.")
        horarios_json = [
            h.model_dump() if hasattr(h, "model_dump")
            else h.dict() if hasattr(h, "dict")
            else h
            for h in horarios
        ]
        return horarios_json
    except Exception as e:
        logger.error(f"[GET /schedules/] Error al listar los horarios: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error al listar los horarios: {str(e)}")

@app.get("/{id}", response_class=JSONResponse)
def obtener_detalle_horario(id: int):
    """
    Obtiene el detalle de un horario por su ID.
    """
    horario = controller.get_by_id(Schedule, id)
    if not horario:
        logger.warning(f"[GET /schedules/{id}] Horario no encontrado.")
        raise HTTPException(status_code=404, detail="Horario no encontrado")
    logger.info(f"[GET /schedules/{id}] Se consultó el horario con ID={id}.")
    if hasattr(horario, "model_dump"):
        return horario.model_dump()
    elif hasattr(horario, "dict"):
        return horario.dict()
    else:
        return horario