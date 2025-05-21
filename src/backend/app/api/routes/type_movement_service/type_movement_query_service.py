import logging
from fastapi import APIRouter, Security, Query, HTTPException
from fastapi.responses import JSONResponse

from backend.app.core.auth import get_current_user
from backend.app.models.type_movement import TypeMovementOut
from backend.app.logic.universal_controller_instance import universal_controller as controller

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

router = APIRouter(prefix="/typemovement", tags=["typemovement"])

@router.get("/consultar", response_class=JSONResponse)
def consultar(
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    """
    Mensaje para consulta de tipo de movimiento.
    """
    return JSONResponse(content={"message": "Consulta de tipo de movimiento habilitada."})

@router.get("/typemovements", response_class=JSONResponse)
def get_typemovement(
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    """
    Devuelve todos los tipos de movimiento registrados.
    """
    typemovements = controller.read_all(TypeMovementOut)
    logger.info(f"[GET /typemovements] Número de tipos de movimiento encontrados: {len(typemovements) if typemovements else 0}")
    return JSONResponse(content={"typemovements": typemovements or []})

@router.get("/tipomovimiento", response_class=JSONResponse)
def typemovement(
    id: int = Query(...),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    """
    Devuelve un tipo de movimiento por su ID.
    """
    unit_typemovement = controller.get_by_column(TypeMovementOut, "ID", id)
    if not unit_typemovement:
        logger.warning(f"[GET /tipomovimiento] No se encontró tipo de movimiento con id={id}")
        raise HTTPException(status_code=404, detail="Tipo de movimiento no encontrado")
    return JSONResponse(content=unit_typemovement.model_dump())