import logging
from fastapi import APIRouter, Form, Security
from fastapi.responses import JSONResponse
from backend.app.logic.universal_controller_instance import universal_controller as controller
from backend.app.models.maintainance_status import MaintainanceStatus
from backend.app.core.auth import get_current_user

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

app = APIRouter(prefix="/maintainance_status", tags=["maintainance_status"])

@app.post("/create", response_class=JSONResponse)
def crear_estado_mantenimiento(
    ID: str = Form(...),
    TipoEstado: str = Form(...),
    #current_user: dict = Security(get_current_user, scopes=["system", "mantenimiento"])
):
    """
    Crea un nuevo estado de mantenimiento.
    """
    try:
        nuevo_estado = MaintainanceStatus(ID=ID, TipoEstado=TipoEstado)
        controller.add(nuevo_estado)
        logger.info(f"[POST /maintainance_status/create] Estado de mantenimiento creado: {nuevo_estado}")
        return JSONResponse(
            status_code=200,
            content={"message": "Estado de mantenimiento creado exitosamente."}
        )
    except Exception as e:
        logger.warning(f"[POST /maintainance_status/create] Error al crear estado: {str(e)}")
        return JSONResponse(
            status_code=400,
            content={"detail": f"Error al crear estado: {str(e)}"}
        )

@app.post("/update", response_class=JSONResponse)
def actualizar_estado(
    id: int = Form(...),
    TipoEstado: str = Form(...),
    #current_user: dict = Security(get_current_user, scopes=["system", "mantenimiento"])
):
    """
    Actualiza un estado de mantenimiento existente.
    """
    existing_estado = controller.get_by_id(MaintainanceStatus, id)
    if not existing_estado:
        logger.warning(f"[POST /maintainance_status/update] Estado de mantenimiento no encontrado: ID={id}")
        return JSONResponse(
            status_code=404,
            content={"detail": "Estado de mantenimiento no encontrado"}
        )

    estado_actualizado = MaintainanceStatus(ID=id, TipoEstado=TipoEstado)
    try:
        controller.update(estado_actualizado)
        logger.info(f"[POST /maintainance_status/update] Estado de mantenimiento actualizado: {estado_actualizado}")
        return JSONResponse(
            status_code=200,
            content={"message": "Estado de mantenimiento actualizado exitosamente.", "data": estado_actualizado.to_dict()}
        )
    except Exception as e:
        logger.warning(f"[POST /maintainance_status/update] Error al actualizar estado: {str(e)}")
        return JSONResponse(
            status_code=400,
            content={"detail": f"Error al actualizar estado: {str(e)}"}
        )

@app.post("/delete", response_class=JSONResponse)
def eliminar_estado(
    id: int = Form(...),
    #current_user: dict = Security(get_current_user, scopes=["system", "mantenimiento"])
):
    """
    Elimina un estado de mantenimiento por su ID.
    """
    existing_estado = controller.get_by_id(MaintainanceStatus, id)
    if not existing_estado:
        logger.warning(f"[POST /maintainance_status/delete] Estado de mantenimiento no encontrado: ID={id}")
        return JSONResponse(
            status_code=404,
            content={"detail": "Estado de mantenimiento no encontrado"}
        )

    try:
        controller.delete(existing_estado)
        logger.info(f"[POST /maintainance_status/delete] Estado de mantenimiento eliminado: ID={id}")
        return JSONResponse(
            status_code=200,
            content={"message": "Estado de mantenimiento eliminado exitosamente."}
        )
    except Exception as e:
        logger.warning(f"[POST /maintainance_status/delete] Error al eliminar estado: {str(e)}")
        return JSONResponse(
            status_code=400,
            content={"detail": f"Error al eliminar estado: {str(e)}"}
        )