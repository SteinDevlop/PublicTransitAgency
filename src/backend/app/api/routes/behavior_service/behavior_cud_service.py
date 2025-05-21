import logging
from fastapi import (
    Form, HTTPException, APIRouter, Security, status
)
from fastapi.responses import JSONResponse

from backend.app.models.behavior import BehaviorCreate, BehaviorOut
from backend.app.logic.universal_controller_instance import universal_controller as controller
from backend.app.core.auth import get_current_user

# Configuración de logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

router = APIRouter(prefix="/behavior", tags=["behavior"])

@router.get("/supervisor/crear", response_class=JSONResponse)
def index_create_supervisor(
    current_user: dict = Security(
        get_current_user,
        scopes=["system", "administrador", "pasajero"])
):
    """
    Devuelve el próximo ID disponible para supervisor y la lista de behaviors.
    """
    try:
        behaviors = controller.read_all(BehaviorOut)
        ultimo_id = max(p["ID"] for p in behaviors) if behaviors else 0
        nuevo_id = ultimo_id + 1
        return JSONResponse(
            content={
                "nuevo_id": nuevo_id,
                "behaviors": behaviors
            }
        )
    except Exception as e:
        logger.error(f"Error al obtener el último ID: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": f"Error al obtener el último ID: {str(e)}"}
        )

@router.get("/administrador/crear", response_class=JSONResponse)
def index_create_admin(
    current_user: dict = Security(
        get_current_user,
        scopes=["system", "administrador", "pasajero"])
):
    """
    Devuelve el próximo ID disponible para administrador y la lista de behaviors.
    """
    try:
        behaviors = controller.read_all(BehaviorOut)
        ultimo_id = max(p["ID"] for p in behaviors) if behaviors else 0
        nuevo_id = ultimo_id + 1
        return JSONResponse(
            content={
                "nuevo_id": nuevo_id,
                "behaviors": behaviors
            }
        )
    except Exception as e:
        logger.error(f"Error al obtener el último ID: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": f"Error al obtener el último ID: {str(e)}"}
        )

@router.get("/administrador/actualizar", response_class=JSONResponse)
def index_update(
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "supervisor"])
):
    """
    Devuelve un mensaje indicando que se debe mostrar el formulario de actualización (JSON).
    """
    return JSONResponse(content={"message": "Mostrar formulario de actualización de rendimiento."})

@router.get("/administrador/eliminar", response_class=JSONResponse)
def index_delete(
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    """
    Devuelve un mensaje indicando que se debe mostrar el formulario de eliminación (JSON).
    """
    return JSONResponse(content={"message": "Mostrar formulario de eliminación de rendimiento."})

@router.post("/create", response_class=JSONResponse)
async def create_behavior(
    ID: int = Form(...),
    iduser: int = Form(...),
    cantidadrutas: int = Form(...),
    horastrabajadas: int = Form(...),
    observaciones: str = Form(...),
    fecha: str = Form(...),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    #logger.info(f"[POST /create] Behavior: {current_user['user_id']} - Intentando crear rendimiento con ID: {ID}")

    try:
        existing_behavior = controller.get_by_id(BehaviorOut, ID)
        if existing_behavior:
            logger.warning(f"[POST /create] Error de validación: El rendimiento ya existe con identificación {ID}")
            raise HTTPException(400, detail="El rendimiento ya existe con la misma identificación.")

        new_behavior = BehaviorCreate(
            ID=ID,
            iduser=iduser,
            cantidadrutas=cantidadrutas,
            horastrabajadas=horastrabajadas,
            observaciones=observaciones,
            fecha=fecha
        )
        controller.add(new_behavior)
        logger.info(f"[POST /create] Rendimiento creado exitosamente con identificación {ID}")
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "operation": "create",
                "success": True,
                "data": BehaviorOut(
                    ID=new_behavior.ID,
                    iduser=new_behavior.iduser,
                    cantidadrutas=new_behavior.cantidadrutas,
                    horastrabajadas=new_behavior.horastrabajadas,
                    observaciones=new_behavior.observaciones,
                    fecha=new_behavior.fecha
                ).model_dump(),
                "message": "Behavior created successfully."
            }
        )
    except ValueError as e:
        logger.warning(f"[POST /create] Error de validación: {str(e)}")
        raise HTTPException(400, detail=str(e))
    except Exception as e:
        logger.error(f"[POST /create] Error interno: {str(e)}")
        raise HTTPException(500, detail=f"Internal server error: {str(e)}")

@router.post("/update", response_class=JSONResponse)
async def update_behavior(
    ID: int = Form(...),
    iduser: int = Form(...),
    cantidadrutas: int = Form(...),
    horastrabajadas: int = Form(...),
    observaciones: str = Form(...),
    fecha: str = Form(...),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    #logger.info(f"[POST /update] Rendimiento: {current_user['user_id']} - Actualizando rendimiento ID={ID}")
    try:
        existing = controller.get_by_column(BehaviorOut, "ID", ID)
        if existing is None:
            logger.warning(f"[POST /update] Rendimiento no encontrada: ID={ID}")
            raise HTTPException(404, detail="Behavior not found")

        updated_behavior = BehaviorOut(
            ID=ID,
            iduser=iduser,
            cantidadrutas=cantidadrutas,
            horastrabajadas=horastrabajadas,
            observaciones=observaciones,
            fecha=fecha
        )
        controller.update(updated_behavior)
        logger.info(f"[POST /update] Rendimiento actualizada exitosamente: {updated_behavior}")
        return JSONResponse(
            content={
                "operation": "update",
                "success": True,
                "data": updated_behavior.model_dump(),
                "message": f"Behavior {ID} updated successfully."
            }
        )
    except ValueError as e:
        logger.warning(f"[POST /update] Error de validación: {str(e)}")
        raise HTTPException(400, detail=str(e))

@router.post("/delete", response_class=JSONResponse)
async def delete_behavior(
    ID: int = Form(...),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    #logger.info(f"[POST /delete] Rendimiento: {current_user['user_id']} - Eliminando rendimiento ID={ID}")
    try:
        existing = controller.get_by_column(BehaviorOut, "ID", ID)
        if not existing:
            logger.warning(f"[POST /delete] Rendimiento no encontrado en la base de datos: ID={ID}")
            raise HTTPException(404, detail="Behavior not found")

        controller.delete(existing)
        logger.info(f"[POST /delete] Rendimiento eliminada exitosamente: ID={ID}")
        return JSONResponse(
            content={
                "operation": "delete",
                "success": True,
                "message": f"Behavior {ID} deleted successfully."
            }
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"[POST /delete] Error interno: {str(e)}")
        raise HTTPException(500, detail=f"Internal server error: {str(e)}")