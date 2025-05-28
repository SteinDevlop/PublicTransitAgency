import logging
from fastapi import APIRouter, Security, Query, HTTPException, status
from fastapi.responses import JSONResponse

from backend.app.core.auth import get_current_user
from backend.app.models.user import UserOut
from backend.app.logic.universal_controller_instance import universal_controller as controller

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

router = APIRouter(prefix="/user", tags=["user"])

@router.get("/consultar", response_class=JSONResponse)
def consultar():
    """
    Mensaje de consulta de usuarios.
    """
    return JSONResponse(content={"message": "Consulta de usuarios habilitada."})

@router.get("/users", response_class=JSONResponse)
async def get_users():
    """
    Devuelve todos los usuarios registrados.
    """
    usuarios = controller.read_all(UserOut)
    logger.info(f"[GET /users] Número de usuarios encontrados: {len(usuarios) if usuarios else 0}")
    return JSONResponse(content={"usuarios": usuarios or [],"cantidad":len(usuarios)})

@router.get("/usuario", response_class=JSONResponse)
def usuario(
    id: int = Query(...),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "pasajero"])
):
    """
    Devuelve un usuario por su ID.
    """
    unit_usuario = controller.get_by_column(UserOut, "ID", id)
    if unit_usuario:
        logger.info(f"[GET /usuario] Usuario encontrado: {unit_usuario.ID}")
        return JSONResponse(content=unit_usuario.model_dump())
    else:
        logger.warning(f"[GET /usuario] No se encontró usuario con id={id}")
        raise HTTPException(status_code=404, detail="Usuario no encontrado")