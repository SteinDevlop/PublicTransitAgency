import logging
from fastapi import APIRouter, HTTPException, Security
from fastapi.responses import JSONResponse
from backend.app.logic.universal_controller_instance import universal_controller as controller

from backend.app.models.shift import Shift
from backend.app.core.auth import get_current_user

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

app = APIRouter(prefix="/shifts", tags=["shifts"])

@app.get("/", response_class=JSONResponse)
def listar_turnos():
    """
    Consulta la lista de todos los turnos.
    """
    try:
        turnos = controller.read_all(Shift)
        logger.info(f"[GET /shifts/] Se listaron {len(turnos)} turnos.")
        turnos_json = [
            t.model_dump() if hasattr(t, "model_dump")
            else t.dict() if hasattr(t, "dict")
            else t
            for t in turnos
        ]
        return turnos_json
    except Exception as e:
        logger.error(f"[GET /shifts/] Error al listar turnos: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/turnos", response_class=JSONResponse)
async def get_users():
    """
    Devuelve todos los usuarios registrados.
    """
    turnos = controller.read_all(Shift)
    logger.info(f"[GET /users] Número de usuarios encontrados: {len(turnos) if turnos else 0}")
    return JSONResponse(content={"turnos": turnos or []})

@app.get("/{id}", response_class=JSONResponse)
def detalle_turno(id: int):
    """
    Consulta el detalle de un turno en específico por su ID.
    """
    try:
        turno = controller.get_by_id(Shift, id)
        if not turno:
            logger.warning(f"[GET /shifts/{id}] Turno no encontrado.")
            raise HTTPException(status_code=404, detail="Turno no encontrado")
        logger.info(f"[GET /shifts/{id}] Se consultó el turno con ID={id}.")
        if hasattr(turno, "model_dump"):
            return turno.model_dump()
        elif hasattr(turno, "dict"):
            return turno.dict()
        else:
            return turno
    except Exception as e:
        logger.error(f"[GET /shifts/{id}] Error al consultar turno: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))