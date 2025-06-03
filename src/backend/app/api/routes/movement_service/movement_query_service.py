import logging
from fastapi import APIRouter, Query, Security, status
from fastapi.responses import JSONResponse
from backend.app.core.auth import get_current_user
from backend.app.models.movement import MovementOut
from backend.app.logic.universal_controller_instance import universal_controller as controller

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

router = APIRouter(prefix="/movement", tags=["movement"])

@router.get("/pasajero/movements", response_class=JSONResponse)
async def get_all_pasajero_movements():
    """
    Returns all movement records as JSON for passenger.
    """
    movimientos = controller.read_all(MovementOut)
    logger.info(f"[GET /pasajero/movements] Número de Movimientos encontrados: {len(movimientos)}")
    # Convert to dicts if needed
    movimientos_dicts = [m.model_dump() if hasattr(m, "model_dump") else m.dict() if hasattr(m, "dict") else m for m in movimientos]
    return JSONResponse(content=movimientos_dicts)

@router.get("/administrador/movements", response_class=JSONResponse)
async def get_all_admin_movements():
    """
    Returns all movement records as JSON for administrator.
    """
    movimientos = controller.read_all(MovementOut)
    logger.info(f"[GET /administrador/movements] Número de Movimientos encontrados: {len(movimientos)}")
    movimientos_dicts = [m.model_dump() if hasattr(m, "model_dump") else m.dict() if hasattr(m, "dict") else m for m in movimientos]
    return JSONResponse(content=movimientos_dicts)

@router.get("/administrador/byid", response_class=JSONResponse)
async def get_movement_by_id(
    ID: int = Query(...),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    """
    Returns a movement by its ID as JSON. Requires administrator scope.
    """
    result = controller.get_by_column(MovementOut, "ID", ID)
    if result:
        return JSONResponse(content=result.model_dump() if hasattr(result, "model_dump") else result.dict())
    else:
        logger.warning(f"[GET /administrador/byid] No se encontró movimiento con id={ID}")
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": f"Movimiento con id={ID} no encontrado"}
        )

@router.get("/pasajero/bycardid", response_class=JSONResponse)
async def get_movement_by_cardid(
    ID: int = Query(...),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador","pasajero"])
):
    result = controller.get_by_column(MovementOut, "IDTarjeta", ID)
    if result:
        # Always return a list
        if isinstance(result, list):
            movements = [r.model_dump() if hasattr(r,"model_dump") else r.dict() if hasattr(r,"dict") else r for r in result]
        else:
            movements = [result.model_dump() if hasattr(result,"model_dump") else result.dict() if hasattr(result,"dict") else result]
        return JSONResponse(content=movements)
    else:
        logger.warning(f"[GET /administrador/cardbyid] No se encontró movimiento con id={ID}")
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=[]
        )