import logging
from fastapi import (
    Form, HTTPException, APIRouter, Security, status
)
from fastapi.responses import JSONResponse

from backend.app.models.type_movement import TypeMovementCreate, TypeMovementOut
from backend.app.logic.universal_controller_instance import universal_controller as controller
from backend.app.core.auth import get_current_user

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

router = APIRouter(prefix="/typemovement", tags=["typemovement"])

@router.get("/crear", response_class=JSONResponse)
def index_create(
    current_user: dict = Security(
        get_current_user, scopes=["system", "administrador"])
):
    return JSONResponse(content={"message": "Formulario de creación de tipo de movimiento habilitado."})

@router.get("/actualizar", response_class=JSONResponse)
def index_update(
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    return JSONResponse(content={"message": "Formulario de actualización de tipo de movimiento habilitado."})

@router.get("/eliminar", response_class=JSONResponse)
def index_delete(
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    return JSONResponse(content={"message": "Formulario de eliminación de tipo de movimiento habilitado."})

@router.post("/create", response_class=JSONResponse)
async def create_typemovement(
    ID: int = Form(...),
    TipoMovimiento: str = Form(...),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    try:
        existing = controller.get_by_column(TypeMovementOut, "TipoMovimiento", TipoMovimiento)
        if existing:
            logger.warning(f"[POST /create] Error de validación: El tipo de movimiento ya existe con ID {ID}")
            raise HTTPException(400, detail="El tipo de movimiento ya existe con la misma identificación.")

        new_typemovement = TypeMovementCreate(ID=ID, TipoMovimiento=TipoMovimiento)
        logger.info(f"Intentando insertar tipo de movimiento con datos: {new_typemovement.model_dump()}")
        controller.add(new_typemovement)
        logger.info(f"Tipo de Movimiento insertado con ID: {new_typemovement.ID}")
        logger.info(f"[POST /create] Tipo de Movimiento creado exitosamente con identificación {ID}")
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "operation": "create",
                "success": True,
                "data": TypeMovementOut(ID=new_typemovement.ID, TipoMovimiento=new_typemovement.TipoMovimiento).model_dump(),
                "message": "TypeMovement created successfully."
            }
        )
    except ValueError as e:
        logger.warning(f"[POST /create] Error de validación: {str(e)}")
        raise HTTPException(400, detail=str(e))
    except Exception as e:
        logger.error(f"[POST /create] Error interno: {str(e)}")
        raise HTTPException(500, detail=f"Internal server error: {str(e)}")

@router.post("/update", response_class=JSONResponse)
async def update_typemovement(
    ID: int = Form(...),
    TipoMovimiento: str = Form(...),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    try:
        existing = controller.get_by_id(TypeMovementOut, ID)
        if existing is None:
            logger.warning(f"[POST /update] Tipo de Movimiento no encontrado: ID={ID}")
            raise HTTPException(404, detail="TypeMovement not found")

        updated_typemovement = TypeMovementOut(ID=ID, TipoMovimiento=TipoMovimiento)
        controller.update(updated_typemovement)
        logger.info(f"[POST /update] TipoMovimiento actualizada exitosamente: {updated_typemovement}")
        return JSONResponse(
            content={
                "operation": "update",
                "success": True,
                "data": updated_typemovement.model_dump(),
                "message": f"TypeMovement {ID} updated successfully."
            }
        )
    except ValueError as e:
        logger.warning(f"[POST /update] Error de validación: {str(e)}")
        raise HTTPException(400, detail=str(e))

@router.post("/delete", response_class=JSONResponse)
async def delete_typemovement(
    ID: int = Form(...),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    try:
        existing = controller.get_by_id(TypeMovementOut, ID)
        if not existing:
            logger.warning(f"[POST /delete] Tipo de Movimiento no encontrado en la base de datos: ID={ID}")
            raise HTTPException(404, detail="TypeMovement not found")

        logger.info(f"[POST /delete] Eliminando tipo de movimiento con ID={ID}")
        controller.delete(existing)
        logger.info(f"[POST /delete] Tipo de Movimiento eliminada exitosamente: ID={ID}")
        return JSONResponse(
            content={
                "operation": "delete",
                "success": True,
                "message": f"TypeMovement {ID} deleted successfully."
            }
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"[POST /delete] Error interno: {str(e)}")
        raise HTTPException(500, detail=f"Internal server error: {str(e)}")