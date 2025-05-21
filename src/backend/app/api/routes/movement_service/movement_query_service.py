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
    # Si movimientos ya son dicts, devuélvelos directamente
    return JSONResponse(content=movimientos)

@router.get("/administrador/movements", response_class=JSONResponse)
async def get_all_admin_movements():
    """
    Returns all movement records as JSON for administrator.
    """
    movimientos = controller.read_all(MovementOut)
    logger.info(f"[GET /administrador/movements] Número de Movimientos encontrados: {len(movimientos)}")
    # Si movimientos ya son dicts, devuélvelos directamente
    return JSONResponse(content=movimientos)

@router.get("/administrador/byid", response_class=JSONResponse)
async def get_movement_by_id(
    ID: int = Query(...),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    """
    Returns a movement by its ID as JSON. Requires administrator scope.
    """
    #logger.info(f"[GET /administrador/byid] Usuario: {current_user['user_id']} - Consultando movimiento con id={ID}")
    result = controller.get_by_column(MovementOut, "ID", ID)
    if result:
        # Si result ya es dict, devuélvelo directamente
        return JSONResponse(content=result.to_dict())
    else:
        logger.warning(f"[GET /administrador/byid] No se encontró movimiento con id={ID}")
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": f"Movimiento con id={ID} no encontrado"}
        )