import logging
from fastapi import APIRouter, Security, Query, status, HTTPException
from fastapi.responses import JSONResponse

from backend.app.core.auth import get_current_user
from backend.app.models.behavior import BehaviorOut
from backend.app.logic.universal_controller_instance import universal_controller as controller

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

router = APIRouter(prefix="/behavior", tags=["behavior"])

@router.get("/administrador/consultar", response_class=JSONResponse)
def consultar_administrador(
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    """
    Retorna un mensaje indicando acceso a la consulta de rendimientos para el administrador.
    """
    #logger.info(f"[GET /administrador/consultar] Usuario: {current_user['user_id']} - Consulta de rendimientos (admin)")
    return JSONResponse(content={"message": "Consulta de rendimientos para administrador habilitada."})

@router.get("/supervisor/consultar", response_class=JSONResponse)
def consultar_supervisor(
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    """
    Retorna un mensaje indicando acceso a la consulta de rendimientos para el supervisor.
    """
    #logger.info(f"[GET /supervisor/consultar] Usuario: {current_user['user_id']} - Consulta de rendimientos (supervisor)")
    return JSONResponse(content={"message": "Consulta de rendimientos para supervisor habilitada."})

@router.get("/supervisor/behaviors", response_class=JSONResponse)
def get_behaviors_supervisor(
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    """
    Devuelve todos los registros de behaviors para supervisor.
    """
    #logger.info(f"[GET /supervisor/behaviors] Usuario: {current_user['user_id']} - Consultando behaviors (supervisor).")
    behaviors = controller.read_all(BehaviorOut)
    return JSONResponse(content={"behaviors": behaviors or []})

@router.get("/administrador/behaviors", response_class=JSONResponse)
def get_behaviors_admin(
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    """
    Devuelve todos los registros de behaviors para administrador.
    """
    #logger.info(f"[GET /administrador/behaviors] Usuario: {current_user['user_id']} - Consultando behaviors (admin).")
    behaviors = controller.read_all(BehaviorOut)
    return JSONResponse(content={"behaviors": behaviors or []})

@router.get("/rendimientos", response_class=JSONResponse)
def get_rendimientos(
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    """
    Devuelve todos los registros de rendimientos.
    """
    #logger.info(f"[GET /rendimientos] Usuario: {current_user['user_id']} - Consultando todos los rendimientos.")
    rendimientos = controller.read_all(BehaviorOut)
    logger.info(f"[GET /rendimientos] Número de rendimientos encontrados: {len(rendimientos)}")
    return JSONResponse(content={"rendimientos": rendimientos or []})

@router.get("/byid", response_class=JSONResponse)
def rendimiento_by_id(
    ID: int = Query(...),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    """
    Devuelve un rendimiento por su ID. Si no se encuentra, retorna 404.
    """
    #logger.info(f"[GET /byid] Usuario: {current_user['user_id']} - Consultando rendimiento ID={ID}")
    unit_rendimiento = controller.get_by_id(BehaviorOut, ID)
    if unit_rendimiento:
        logger.info(f"[GET /byid] Rendimiento encontrado: {unit_rendimiento.ID}, iduser: {unit_rendimiento.iduser}")
        return JSONResponse(content=unit_rendimiento.model_dump())
    else:
        logger.warning(f"[GET /byid] No se encontró rendimiento con ID={ID}")
        raise HTTPException(status_code=404, detail="Rendimiento no encontrado")

@router.get("/byuser", response_class=JSONResponse)
def rendimiento_by_user(
    iduser: int = Query(...),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "supervisor"])
):
    """
    Devuelve todos los rendimientos por usuario. Si no se encuentra, retorna una lista vacía.
    """
    #logger.info(f"[GET /byuser] Usuario: {current_user['user_id']} - Consultando rendimientos por iduser={iduser}")
    unit_rendimiento = controller.get_by_column(BehaviorOut, column_name="iduser", value=iduser)
    return JSONResponse(content={"rendimientos": unit_rendimiento or []})