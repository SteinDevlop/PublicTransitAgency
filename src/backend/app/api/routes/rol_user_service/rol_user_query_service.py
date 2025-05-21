import logging
from fastapi import APIRouter, Security, Query, HTTPException
from fastapi.responses import JSONResponse

from backend.app.core.auth import get_current_user
from backend.app.models.rol_user import RolUserOut
from backend.app.logic.universal_controller_instance import universal_controller as controller

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

router = APIRouter(prefix="/roluser", tags=["roluser"])

@router.get("/administrador/consultar", response_class=JSONResponse)
def consultar():
    """
    Mensaje de consulta de rol de usuario.
    """
    return JSONResponse(content={"message": "Consulta de rol de usuario habilitada."})

@router.get("/administrador/rolusers", response_class=JSONResponse)
def get_rolusers():
    """
    Devuelve todos los roles de usuario registrados.
    """
    rolusers = controller.read_all(RolUserOut)
    logger.info(f"[GET /rolusers] Número de roles de usuario encontrados: {len(rolusers) if rolusers else 0}")
    return JSONResponse(content={"rolusers": rolusers or []})

@router.get("/administrador/tipousuario", response_class=JSONResponse)
def roluser(
    ID: int = Query(...),
):
    """
    Devuelve un rol de usuario por su ID.
    """
    unit_roluser = controller.get_by_id(RolUserOut, ID)
    if not unit_roluser:
        logger.warning(f"[GET /tipousuario] No se encontró rol usuario con id={ID}")
        raise HTTPException(status_code=404, detail="Rol Usuario no encontrado")

    logger.info(f"[GET /tipousuario] Rol de Usuario encontrado: {unit_roluser.ID}, {unit_roluser.Rol}")
    return JSONResponse(content=unit_roluser.model_dump())