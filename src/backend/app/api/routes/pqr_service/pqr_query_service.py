import logging
from fastapi import APIRouter, Security, Query, HTTPException
from fastapi.responses import JSONResponse

from backend.app.core.auth import get_current_user
from backend.app.models.pqr import PQROut
from backend.app.logic.universal_controller_instance import universal_controller as controller

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

router = APIRouter(prefix="/pqr", tags=["pqr"])

@router.get("/consultar/administrador", response_class=JSONResponse)
def consultar_admin(
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "pasajero"])
):
    """
    Mensaje de consulta de PQR para administrador.
    """
    return JSONResponse(content={"message": "Consulta de PQR vía administrador habilitada."})

@router.get("/consultar/pasajero", response_class=JSONResponse)
def consultar_pasajero(
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    """
    Mensaje de consulta de PQR para pasajero.
    """
    return JSONResponse(content={"message": "Consulta de PQR vía pasajero habilitada."})

@router.get("/pasajero/pqrs", response_class=JSONResponse)
def get_pqrs_pasajero(
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    """
    Devuelve todos los registros de PQR para pasajero.
    """
    pqrs = controller.read_all(PQROut)
    logger.info(f"[GET /pasajero/pqrs] Número de PQRs encontrados: {len(pqrs) if pqrs else 0}")
    return JSONResponse(content={"pqrs": pqrs or [], "cantidad":len(pqrs)})

@router.get("/administrador/pqrs", response_class=JSONResponse)
def get_pqrs_admin(
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    """
    Devuelve todos los registros de PQR para administrador.
    """
    pqrs = controller.read_all(PQROut)
    logger.info(f"[GET /administrador/pqrs] Número de PQRs encontrados: {len(pqrs) if pqrs else 0}")
    return JSONResponse(content={"pqrs": pqrs or [], "cantidad":len(pqrs)})

@router.get("/find", response_class=JSONResponse)
def pqr_by_id(
    ID: int = Query(...),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    """
    Devuelve un PQR por su ID.
    """
    unit_pqr = controller.get_by_column(PQROut, "ID", ID)
    if unit_pqr:
        logger.info(f"[GET /find] PQR encontrada: {unit_pqr.ID}")
        return JSONResponse(content=unit_pqr.model_dump())
    else:
        logger.warning(f"[GET /find] No se encontró PQR con ID={ID}")
        raise HTTPException(status_code=404, detail="PQR not found")

@router.get("/user", response_class=JSONResponse)
def pqr_by_user(
    iduser: int = Query(...),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "pasajero"])
):
    """
    Devuelve la(s) PQR(s) por ID de usuario.
    """
    pqrs = controller.get_by_column(PQROut, column_name="identificationuser", value=iduser)
    if pqrs:
        logger.info(f"[GET /user] PQR encontrada(s) para iduser: {iduser}")
        # Si trae un solo resultado, lo devolvemos como objeto, si es lista, como lista
        if isinstance(pqrs, list):
            return JSONResponse(content={"pqrs": [p.model_dump() for p in pqrs]})
        else:
            return JSONResponse(content=pqrs.model_dump())
    else:
        logger.warning(f"[GET /user] No se encontró PQR con iduser={iduser}")
        raise HTTPException(status_code=404, detail="PQR not found")