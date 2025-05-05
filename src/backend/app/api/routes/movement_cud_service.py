#movement_cud_service.py
# This file contains the CRUD operations for the Movement model using FastAPI.
# It includes routes for creating, updating, and deleting movements.
# The routes are designed to handle form submissions and return appropriate responses.

import logging
from fastapi import FastAPI, Form, HTTPException, APIRouter, Request, Depends, status, Query, Security
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from backend.app.models.movement import MovementCreate, MovementOut  # Make sure your models are in this file
from backend.app.logic.universal_controller_postgres import UniversalController
from backend.app.core.auth import get_current_user 
import uvicorn

# Configuración de logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

app = APIRouter(prefix="/movement", tags=["movement"])  # Initialize the API router with the given prefix and tag
templates = Jinja2Templates(directory="src/backend/app/templates")  # Set up the template directory

def get_controller():
    """
    Dependency to get the controller instance.
    """
    return UniversalController()

# Route to display the "Create Movement" form
@app.get("/crear", response_class=HTMLResponse)
def index_create(
    request: Request,
    current_user: dict = Security(
        get_current_user,
        scopes=["system", "administrador"]
    )
):
    """
    Render the 'CrearMovimiento.html' template for creating a movement.
    """
    logger.info(f"[GET /crear] Usuario: {current_user['user_id']} - Mostrando formulario de creación de movimiento")
    return templates.TemplateResponse("CrearMovimiento.html", {"request": request})

# Route to display the "Update Movement" form
@app.get("/actualizar", response_class=HTMLResponse)
def index_update(
    request: Request,
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    """
    Render the 'ActualizarMovimiento.html' template for updating a movement.
    """
    logger.info(f"[GET /actualizar] Usuario: {current_user['user_id']} - Mostrando formulario de actualización de movimiento")
    return templates.TemplateResponse("ActualizarMovimiento.html", {"request": request})

# Route to display the "Delete Movement" form
@app.get("/eliminar", response_class=HTMLResponse)
def index_delete(
    request: Request,
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    """
    Render the 'EliminarMovimiento.html' template for deleting a movement.
    """
    logger.info(f"[GET /eliminar] Usuario: {current_user['user_id']} - Mostrando formulario de eliminación de movimiento")
    return templates.TemplateResponse("EliminarMovimiento.html", {"request": request})

# Route to create a new movement
@app.post("/create")
async def create_movement(
    id: int = Form(...),
    type: str = Form(...),
    amount: float = Form(...),
    controller: UniversalController = Depends(get_controller),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    """
    Creates a new movement with the provided ID , type and amount.
    """
    logger.info(f"[POST /create] Usuario: {current_user['user_id']} - Creando tarjeta: id={id}, tipo={type}, amount={amount}")
    # Validate the input data using the MovementCreate model
    try:
        new_movement = MovementCreate(
            id=id,
            type=type,
            amount=amount,
        )
        # Do not call to_dict() here
        result = controller.add(new_movement)
        logger.info(f"[POST /create] Movimiento creado exitosamente: {new_movement}")
        return {
            "operation": "create",
            "success": True,
            "data": MovementOut(id=new_movement.id, type=new_movement.type, amount=new_movement.amount).dict(),
            "message": "Movement created successfully"
        }
    except ValueError as e:
        logger.warning(f"[POST /create] Error de validación: {str(e)}")
        raise HTTPException(400, detail=str(e))  # Bad request if validation fails
    except Exception as e:
        logger.error(f"[POST /create] Error interno: {str(e)}")
        raise HTTPException(500, detail=f"Internal server error: {str(e)}")  # General server error

# Route to update an existing movement
@app.post("/update")
async def update_movement(
    id: int = Form(...),
    type: str = Form(...),
    amount: float = Form(...),
    controller: UniversalController = Depends(get_controller),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    """
    Updates an existing movement by its ID and new type.
    If the movement does not exist, it returns a 404 error.
    """
    logger.info(f"[POST /update] Usuario: {current_user['user_id']} - Actualizando tarjeta id={id}, nuevo tipo={type}, amount={amount}")
    # Validate the input data using the MovementCreate model
    try:
        # Look for the existing movement to update
        existing = controller.get_by_id(MovementOut, id)  # We use MovementOut for looking up the movement
        if existing is None:
            logger.warning(f"[POST /update] Movimiento no encontrada: id={id}")
            raise HTTPException(404, detail="Movement not found")
        
        # Create a MovementCreate instance to validate the update data
        updated_movement = MovementCreate(
            id=id,
            type=type,
            amount=existing.amount
        )
        # Use the controller to update the movement (convert model to dict)
        result = controller.update(updated_movement)
        
        # Return the updated movement response using MovementOut
        logger.info(f"[POST /update] Movimiento actualizada exitosamente: {updated_movement}")
        return {
            "operation": "update",
            "success": True,
            "data": MovementOut(id=updated_movement.id, type=updated_movement.type, amount=updated_movement.amount).model_dump(),
            "message": f"Movement {id} updated successfully"
        }
    except ValueError as e:
        logger.warning(f"[POST /update] Error de validación: {str(e)}")
        raise HTTPException(400, detail=str(e))  # Bad request if validation fails

# Route to delete a movement by its ID
@app.post("/delete")
async def delete_movement(
    id: int = Form(...),
    controller: UniversalController = Depends(get_controller),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    """
    Deletes an existing movement by its ID.
    If the movement does not exist, it returns a 404 error.
    """
    logger.info(f"[POST /delete] Usuario: {current_user['user_id']} - Eliminando movimiento id={id}")
    try:
        # Look for the movement to delete
        existing = controller.get_by_id(MovementOut, id)  # We use MovementOut for looking up the movement
        if existing is None:
            logger.warning(f"[POST /delete] Movimiento no encontrada: id={id}")
            raise HTTPException(404, detail="Movement not found")
        
        # Use the controller to delete the movement
        controller.delete(existing)
        logger.info(f"[POST /delete] Movimiento eliminada exitosamente: id={id}")
        return {
            "operation": "delete",
            "success": True,
            "message": f"Movement {id} deleted successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"[POST /delete] Error interno: {str(e)}")
        raise HTTPException(500, detail=str(e))  # General server error