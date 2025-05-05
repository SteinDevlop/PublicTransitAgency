import logging
from fastapi import (
    Form, HTTPException, APIRouter, Request, Security
)
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from backend.app.models.movement import MovementCreate, MovementOut
from backend.app.logic.universal_controller_postgres import UniversalController
from backend.app.core.auth import get_current_user

# Configuración de logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

app = APIRouter(prefix="/movement", tags=["movement"])
controller = UniversalController()
templates = Jinja2Templates(directory="src/backend/app/templates")


@app.get("/crear", response_class=HTMLResponse)
def index_create(
    request: Request,
    current_user: dict = Security(
        get_current_user,
        scopes=["system", "administrador"]
    )
):
    logger.info(f"[GET /crear] Movimiento: {current_user['user_id']} - Mostrando formulario de creación de movimiento")
    return templates.TemplateResponse("CrearMovimiento.html", {"request": request})


@app.get("/actualizar", response_class=HTMLResponse)
def index_update(
    request: Request,
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    logger.info(f"[GET /actualizar] Movimiento: {current_user['user_id']} - Mostrando formulario de actualización de movimiento")
    return templates.TemplateResponse("ActualizarMovimiento.html", {"request": request})


@app.get("/eliminar", response_class=HTMLResponse)
def index_delete(
    request: Request,
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    logger.info(f"[GET /eliminar] Movimiento: {current_user['user_id']} - Mostrando formulario de eliminación de movimiento")
    return templates.TemplateResponse("EliminarMovimiento.html", {"request": request})


@app.post("/create")
async def create_movement(
    id: int = Form(...),
    idtype:int= Form(...),
    amount:float=Form(...),
    current_movement: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    logger.info(f"[POST /create] Movimiento: {current_movement['user_id']} - Intentando crear movimiento con id: {id}")

    try:
        # Verificar si el movimiento ya existe
        existing_movement = controller.get_by_column(MovementOut, "id", id)  
        if existing_movement:
            logger.warning(f"[POST /create] Error de validación: El movimiento ya existe con identificación {id}")
            raise HTTPException(400, detail="El movimiento ya existe con la misma identificación.")

        # Crear movimiento
        new_movement = MovementCreate(id=id, idtype=idtype, amount=amount)
        logger.info(f"Intentando insertar movimiento con datos: {new_movement.model_dump()}")
        controller.add(new_movement)
        logger.info(f"Movimiento insertado con ID: {new_movement.id}")  # Verifica si el ID se asigna
        logger.info(f"[POST /create] Movimiento creado exitosamente con identificación {id}")
        return {
            "operation": "create",
            "success": True,
            "data": MovementOut(id=new_movement.id,idtype=new_movement.idtype,amount=new_movement.amount).model_dump(),
            "message": "Movement created successfully."
        }
        
    except ValueError as e:
        logger.warning(f"[POST /create] Error de validación: {str(e)}")
        raise HTTPException(400, detail=str(e))
    except Exception as e:
        logger.error(f"[POST /create] Error interno: {str(e)}")
        raise HTTPException(500, detail=f"Internal server error: {str(e)}")


@app.post("/update")
async def update_movement(
    id: int = Form(...),
    idtype:int=Form(...),
    amount:float=Form(...),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    logger.info(f"[POST /update] Movimiento: {current_user['user_id']} - Actualizando movimiento id={id}")
    try:
        existing = controller.get_by_id(MovementOut, id)
        if existing is None:
            logger.warning(f"[POST /update] Movimiento no encontrada: id={id}")
            raise HTTPException(404, detail="Movement not found")

        updated_movement = MovementOut(id=id, idtype=idtype, amount=amount)
        controller.update(updated_movement)
        logger.info(f"[POST /update] Movimiento actualizada exitosamente: {updated_movement}")
        return {
            "operation": "update",
            "success": True,
            "data": MovementOut(id=id, idtype=updated_movement.idtype,amount=updated_movement.amount).model_dump(),
            "message": f"Movement {id} updated successfully."
        }
    except ValueError as e:
        logger.warning(f"[POST /update] Error de validación: {str(e)}")
        raise HTTPException(400, detail=str(e))



@app.post("/delete")
async def delete_movement(
    id: int = Form(...),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    logger.info(f"[POST /delete] Movimiento: {current_user['user_id']} - Eliminando movimiento id={id}")
    try:
        existing = controller.get_by_id(MovementOut, id)
        if not existing:
            logger.warning(f"[POST /delete] Movimiento no encontrado en la base de datos: id={id}")
            raise HTTPException(404, detail="Movement not found")

        logger.info(f"[POST /delete] Eliminando movimiento con id={id}")
        controller.delete(existing) 
        logger.info(f"[POST /delete] Movimiento eliminada exitosamente: id={id}")
        return {
            "operation": "delete",
            "success": True,
            "message": f"Movement {id} deleted successfully."
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"[POST /delete] Error interno: {str(e)}")
        raise HTTPException(500, detail=f"Internal server error: {str(e)}")
