import logging
from fastapi import (
    Form, HTTPException, APIRouter, Security, status
)
from fastapi.responses import JSONResponse

from backend.app.models.asistance import AsistanceCreate, AsistanceOut
from backend.app.logic.universal_controller_instance import universal_controller as controller
from backend.app.core.auth import get_current_user

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

router = APIRouter(prefix="/asistance", tags=["asistance"])

@router.get("/crear", response_class=JSONResponse)
def index_create(
    current_user: dict = Security(
        get_current_user,
        scopes=["system", "administrador", "supervisor", "tecnico", "conductor"]
    )
):
    #logger.info(f"[GET /crear] Asistencia: {current_user['user_id']} - Mostrando formulario de creación de asistencia")
    return JSONResponse(content={"message": "Formulario de creación de asistencia habilitado."})

@router.get("/actualizar", response_class=JSONResponse)
def index_update(
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    #logger.info(f"[GET /actualizar] Asistencia: {current_user['user_id']} - Mostrando formulario de actualización de asistencia")
    return JSONResponse(content={"message": "Formulario de actualización de asistencia habilitado."})

@router.get("/eliminar", response_class=JSONResponse)
def index_delete(
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    #logger.info(f"[GET /eliminar] Asistencia: {current_user['user_id']} - Mostrando formulario de eliminación de asistencia")
    return JSONResponse(content={"message": "Formulario de eliminación de asistencia habilitado."})

@router.post("/create", response_class=JSONResponse)
async def create_asistance(
    id: int = Form(...),
    iduser: int = Form(...),
    horainicio: str = Form(...),
    horafinal: str = Form(...),
    fecha: str = Form(...),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    #logger.info(f"[POST /create] Asistance: {current_user['user_id']} - Intentando crear asistencia con id: {id}")
    try:
        existing_asistance = controller.get_by_column(AsistanceOut, "ID", id)
        if existing_asistance:
            logger.warning(f"[POST /create] Error de validación: El asistencia ya existe con identificación {id}")
            raise HTTPException(400, detail="El asistencia ya existe con la misma identificación.")

        new_asistance = AsistanceCreate(
            ID=id,
            iduser=iduser,
            horainicio=horainicio,
            horafinal=horafinal,
            fecha=fecha
        )
        logger.info(f"Intentando insertar asistencia con datos: {new_asistance.model_dump()}")
        controller.add(new_asistance)
        logger.info(f"Asistencia insertado con id: {new_asistance.ID}")
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "operation": "create",
                "success": True,
                "data": AsistanceOut(
                    ID=new_asistance.ID,
                    iduser=new_asistance.iduser,
                    horainicio=new_asistance.horainicio,
                    horafinal=new_asistance.horafinal,
                    fecha=new_asistance.fecha
                ).model_dump(),
                "message": "Asistance created successfully."
            }
        )
    except ValueError as e:
        logger.warning(f"[POST /create] Error de validación: {str(e)}")
        raise HTTPException(400, detail=str(e))
    except Exception as e:
        logger.error(f"[POST /create] Error interno: {str(e)}")
        raise HTTPException(500, detail=f"Internal server error: {str(e)}")

@router.post("/update", response_class=JSONResponse)
async def update_asistance(
    id: int = Form(...),
    iduser: int = Form(...),
    horainicio: str = Form(...),
    horafinal: str = Form(...),
    fecha: str = Form(...),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    #logger.info(f"[POST /update] Asistencia: {current_user['user_id']} - Actualizando asistencia id={id}")
    try:
        existing = controller.get_by_column(AsistanceOut, "ID", id)
        if not existing:
            logger.warning(f"[POST /update] Asistencia no encontrada: id={id}")
            raise HTTPException(404, detail="Asistance not found")

        updated_asistance = AsistanceOut(
            ID=id,
            iduser=iduser,
            horainicio=horainicio,
            horafinal=horafinal,
            fecha=fecha
        )
        controller.update(updated_asistance)
        logger.info(f"[POST /update] Asistencia actualizada exitosamente: {updated_asistance}")
        return JSONResponse(
            content={
                "operation": "update",
                "success": True,
                "data": updated_asistance.model_dump(),
                "message": f"Asistance {id} updated successfully."
            }
        )
    except ValueError as e:
        if "No se encontró ningún registro" in str(e):
            raise HTTPException(status_code=404, detail=str(e))
        logger.warning(f"[POST /update] Error de validación: {str(e)}")
        raise HTTPException(400, detail=str(e))

@router.post("/delete", response_class=JSONResponse)
async def delete_asistance(
    id: int = Form(...),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    #logger.info(f"[POST /delete] Asistencia: {current_user['user_id']} - Eliminando asistencia id={id}")
    try:
        existing = controller.get_by_column(AsistanceOut, "ID", id)
        if not existing:
            logger.warning(f"[POST /delete] Asistencia no encontrado en la base de datos: id={id}")
            raise HTTPException(404, detail="Asistance not found")

        controller.delete(existing)
        logger.info(f"[POST /delete] Asistencia eliminada exitosamente: id={id}")
        return JSONResponse(
            content={
                "operation": "delete",
                "success": True,
                "message": f"Asistance {id} deleted successfully."
            }
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"[POST /delete] Error interno: {str(e)}")
        raise HTTPException(500, detail=f"Internal server error: {str(e)}")