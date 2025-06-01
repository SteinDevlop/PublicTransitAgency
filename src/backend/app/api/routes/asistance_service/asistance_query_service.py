import logging
from fastapi import APIRouter, Security, Query, status, HTTPException
from fastapi.responses import JSONResponse

from backend.app.core.auth import get_current_user
from backend.app.models.asistance import AsistanceOut
from backend.app.logic.universal_controller_instance import universal_controller as controller

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

router = APIRouter(prefix="/asistance", tags=["asistance"])

@router.get("/consultar/administrador", response_class=JSONResponse)
def consultar_administrador(
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "conductor", "supervisor", "mantenimiento"])
):
    """
    Mensaje de consulta de asistencias para administrador.
    """
    #logger.info(f"[GET /consultar/administrador] Usuario: {current_user['user_id']} - Consulta asistencias (admin)")
    return JSONResponse(content={"message": "Consulta de asistencias para administrador habilitada."})

@router.get("/consultar/conductor", response_class=JSONResponse)
def consultar_conductor(
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    """
    Mensaje de consulta de asistencias para conductor.
    """
    #logger.info(f"[GET /consultar/conductor] Usuario: {current_user['user_id']} - Consulta asistencias (conductor)")
    return JSONResponse(content={"message": "Consulta de asistencias para conductor habilitada."})

@router.get("/consultar/supervisor", response_class=JSONResponse)
def consultar_supervisor(
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    """
    Mensaje de consulta de asistencias para supervisor.
    """
    #logger.info(f"[GET /consultar/supervisor] Usuario: {current_user['user_id']} - Consulta asistencias (supervisor)")
    return JSONResponse(content={"message": "Consulta de asistencias para supervisor habilitada."})

@router.get("/consultar/tecnico", response_class=JSONResponse)
def consultar_tecnico(
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    """
    Mensaje de consulta de asistencias para tecnico.
    """
    #logger.info(f"[GET /consultar/tecnico] Usuario: {current_user['user_id']} - Consulta asistencias (tecnico)")
    return JSONResponse(content={"message": "Consulta de asistencias para técnico habilitada."})

@router.get("/asistencias", response_class=JSONResponse)
def get_asistencias(
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    """
    Devuelve todas las asistencias.
    """
    #logger.info(f"[GET /asistencias] Usuario: {current_user['user_id']} - Consultando todas las asistencias.")
    asistencias = controller.read_all(AsistanceOut)
    logger.info(f"[GET /asistencias] Número de asistencias encontradas: {len(asistencias)}")
    return JSONResponse(content={"asistencias": asistencias or [], 'count':len(asistencias)})

@router.get("/find", response_class=JSONResponse)
def asistencia_by_id(
    id: int = Query(...),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    """
    Devuelve una asistencia por su ID.
    """
    #logger.info(f"[GET /find] Usuario: {current_user['user_id']} - Consultando asistencia con id={id}")
    unit_asistencia = controller.get_by_id(AsistanceOut, id)
    if unit_asistencia:
        logger.info(f"[GET /find] Asistencia encontrada: {unit_asistencia.ID}")
        return JSONResponse(content=unit_asistencia.model_dump())
    else:
        logger.warning(f"[GET /find] No se encontró asistencia con id={id}")
        raise HTTPException(status_code=404, detail="Asistencia no encontrada")

@router.get("/user", response_class=JSONResponse)
def asistencia_by_user(
    iduser: int = Query(...),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "conductor", "tecnico", "supervisor"])
):
    """
    Devuelve todas las asistencias de un usuario.
    """
    #logger.info(f"[GET /user] Usuario: {current_user['user_id']} - Consultando asistencias con iduser={iduser}")
    asistencias = controller.get_by_column(AsistanceOut, column_name="iduser", value=iduser)
    return JSONResponse(content={"asistencias": asistencias or []})