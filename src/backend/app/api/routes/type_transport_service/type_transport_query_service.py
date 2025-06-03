import logging
from fastapi import APIRouter, Security, Query, HTTPException, status
from fastapi.responses import JSONResponse

from backend.app.core.auth import get_current_user
from backend.app.models.type_transport import TypeTransportOut
from backend.app.logic.universal_controller_instance import universal_controller as controller

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

router = APIRouter(prefix="/typetransport", tags=["typetransport"])

@router.get("/consultar", response_class=JSONResponse)
def consultar():
    """
    Mensaje de consulta de tipo de transporte.
    """
    return JSONResponse(content={"message": "Consulta de tipo de transporte habilitada."})

@router.get("/typetransports", response_class=JSONResponse)
def get_typetransport(
    current_user: dict = Security(get_current_user, scopes=["system", "administrador","pasajero"])
):
    """
    Devuelve todos los tipos de transporte registrados.
    """
    typetransports = controller.read_all(TypeTransportOut)
    logger.info(f"[GET /typetransports] Número de tipo de transportes encontrados: {len(typetransports) if typetransports else 0}")
    return JSONResponse(content={"typetransports": typetransports or []})

@router.get("/tipotransporte", response_class=JSONResponse)
def typetransport(
    id: int = Query(...),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    """
    Devuelve un tipo de transporte por su ID.
    """
    unit_typetransport = controller.get_by_column(TypeTransportOut, "ID", id)
    if not unit_typetransport:
        logger.warning(f"[GET /tipotransporte] No se encontró tipo de transporte con id={id}")
        raise HTTPException(status_code=404, detail="Tipo de transporte no encontrado")
    return JSONResponse(content=unit_typetransport.model_dump())