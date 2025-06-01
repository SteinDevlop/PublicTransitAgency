import logging
from fastapi import (
    Form, HTTPException, APIRouter, Security, status
)
from fastapi.responses import JSONResponse
from backend.app.models.type_movement import TypeMovementOut
from backend.app.models.movement import MovementCreate, MovementOut
from backend.app.logic.universal_controller_instance import universal_controller as controller
from backend.app.core.auth import get_current_user

# Configuración de logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

router = APIRouter(prefix="/movement", tags=["movement"])

@router.get("/administrador/crear", response_class=JSONResponse)
def index_create(
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    """
    Devuelve el próximo ID disponible y todos los tipos de movimientos (JSON).
    """
    try:
        typemovements = controller.read_all(TypeMovementOut)
        movements = controller.read_all(MovementOut)
        ultimo_id = max(p["ID"] for p in movements) if movements else 0
        nuevo_id = ultimo_id + 1
        return JSONResponse(
            content={
                "nuevo_id": nuevo_id,
                "typemovements": typemovements
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
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    """
    Devuelve un mensaje indicando que se debe mostrar el formulario de actualización (JSON).
    """
    return JSONResponse(content={"message": "Mostrar formulario de actualización de movimiento."})

@router.get("/administrador/eliminar", response_class=JSONResponse)
def index_delete(
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    """
    Devuelve un mensaje indicando que se debe mostrar el formulario de eliminación (JSON).
    """
    return JSONResponse(content={"message": "Mostrar formulario de eliminación de movimiento."})

@router.post("/create", response_class=JSONResponse)
async def create_movement(
    ID: int = Form(...),
    IDTipoMovimiento: int = Form(...),
    Monto: float = Form(...),
    IDTarjeta: int = Form(...),
    current_movement: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    """
    Crea un nuevo movimiento. Devuelve JSON con el resultado.
    """
    try:
        existing_movement = controller.get_by_column(MovementOut, "ID", ID)
        if existing_movement:
            logger.warning(f"[POST /create] Error de validación: El movimiento ya existe con identificación {ID}")
            raise HTTPException(400, detail="El movimiento ya existe con la misma identificación.")

        new_movement = MovementCreate(ID=ID, IDTipoMovimiento=IDTipoMovimiento, Monto=Monto, IDTarjeta= IDTarjeta)
        controller.add(new_movement)
        logger.info(f"[POST /create] Movimiento creado exitosamente con identificación {ID}")
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "operation": "create",
                "success": True,
                "data": MovementOut(ID=new_movement.ID, IDTipoMovimiento=new_movement.IDTipoMovimiento, Monto=new_movement.Monto, IDTarjeta=new_movement.IDTarjeta).model_dump(),
                "message": "Movement created successfully."
            }
        )
    except ValueError as e:
        logger.warning(f"[POST /create] Error de validación: {str(e)}")
        raise HTTPException(400, detail=str(e))
    except Exception as e:
        logger.error(f"[POST /create] Error interno: {str(e)}")
        raise HTTPException(500, detail=f"Internal server error: {str(e)}")

@router.post("/update", response_class=JSONResponse)
async def update_movement(
    ID: int = Form(...),
    IDTipoMovimiento: int = Form(...),
    Monto: float = Form(...),
    IDTarjeta: int =Form(...),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    """
    Actualiza un movimiento existente. Devuelve JSON con el resultado.
    """
    try:
        existing = controller.get_by_column(MovementOut, "ID", ID)
        if existing is None:
            logger.warning(f"[POST /update] Movimiento no encontrada: id={ID}")
            raise HTTPException(404, detail="Movement not found")

        updated_movement = MovementOut(ID=ID, IDTipoMovimiento=IDTipoMovimiento, Monto=Monto, IDTarjeta = IDTarjeta)
        controller.update(updated_movement)
        logger.info(f"[POST /update] Movimiento actualizada exitosamente: {updated_movement}")
        return JSONResponse(
            content={
                "operation": "update",
                "success": True,
                "data": updated_movement.model_dump(),
                "message": f"Movement {ID} updated successfully."
            }
        )
    except ValueError as e:
        logger.warning(f"[POST /update] Error de validación: {str(e)}")
        raise HTTPException(400, detail=str(e))

@router.post("/delete", response_class=JSONResponse)
async def delete_movement(
    ID: int = Form(...),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    """
    Elimina un movimiento existente. Devuelve JSON con el resultado.
    """
    try:
        existing = controller.get_by_column(MovementOut, "ID", ID)
        if not existing:
            logger.warning(f"[POST /delete] Movimiento no encontrado en la base de datos: id={ID}")
            raise HTTPException(404, detail="Movement not found")

        controller.delete(existing)
        logger.info(f"[POST /delete] Movimiento eliminada exitosamente: id={ID}")
        return JSONResponse(
            content={
                "operation": "delete",
                "success": True,
                "message": f"Movement {ID} deleted successfully."
            }
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"[POST /delete] Error interno: {str(e)}")
        raise HTTPException(500, detail=f"Internal server error: {str(e)}")