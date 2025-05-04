#movement_cud_service.py
# This file contains the CRUD operations for the Movement model using FastAPI.
# It includes routes for creating, updating, and deleting movements.
# The routes are designed to handle form submissions and return appropriate responses.

from fastapi import FastAPI, Form, HTTPException, APIRouter, Request, Depends, status, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from backend.app.models.movement import MovementCreate, MovementOut  # Make sure your models are in this file
from backend.app.logic.universal_controller_sql import UniversalController 
import uvicorn

app = APIRouter(prefix="/movement", tags=["movement"])  # Initialize the API router with the given prefix and tag
templates = Jinja2Templates(directory="src/backend/app/templates")  # Set up the template directory

def get_controller():
    """
    Dependency to get the controller instance.
    """
    return UniversalController()

# Route to display the "Create Movement" form
@app.get("/crear", response_class=HTMLResponse)
def index(request: Request):
    """
    Displays the form to create a new movement.
    """
    return templates.TemplateResponse("CrearMovimiento.html", {"request": request})

# Route to display the "Update Movement" form
@app.get("/actualizar", response_class=HTMLResponse)
def index(request: Request):
    """
    Displays the form to update an existing movement.
    """
    return templates.TemplateResponse("ActualizarMovimiento.html", {"request": request})

# Route to display the "Delete Movement" form
@app.get("/eliminar", response_class=HTMLResponse)
def index(request: Request):
    """
    Displays the form to delete an existing movement.
    """
    return templates.TemplateResponse("EliminarMovimiento.html", {"request": request})

# Route to create a new movement
@app.post("/create")
async def create_movement(
    id: int = Form(...),
    type: str = Form(...),
    amount: float = Form(...),
    controller: UniversalController = Depends(get_controller)
):
    """
    Creates a new movement with the provided ID , type and amount.
    """
    try:
        new_movement = MovementCreate(
            id=id,
            type=type,
            amount=amount,
        )
        # Do not call to_dict() here
        result = controller.add(new_movement)
        
        return {
            "operation": "create",
            "success": True,
            "data": MovementOut(id=new_movement.id, type=new_movement.type, amount=new_movement.amount).dict(),
            "message": "Movement created successfully"
        }
    except ValueError as e:
        raise HTTPException(400, detail=str(e))  # Bad request if validation fails
    except Exception as e:
        raise HTTPException(500, detail=f"Internal server error: {str(e)}")  # General server error

# Route to update an existing movement
@app.post("/update")
async def update_movement(
    id: int = Form(...),
    type: str = Form(...),
    amount: float = Form(...),
    controller: UniversalController = Depends(get_controller)
):
    """
    Updates an existing movement by its ID and new type.
    If the movement does not exist, it returns a 404 error.
    """
    try:
        # Look for the existing movement to update
        existing = controller.get_by_id(MovementOut, id)  # We use MovementOut for looking up the movement
        if not existing:
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
        return {
            "operation": "update",
            "success": True,
            "data": MovementOut(id=updated_movement.id, type=updated_movement.type, amount=updated_movement.amount).dict(),
            "message": f"Movement {id} updated successfully"
        }
    except ValueError as e:
        raise HTTPException(400, detail=str(e))  # Bad request if validation fails

# Route to delete a movement by its ID
@app.post("/delete")
async def delete_movement(
    id: int = Form(...),
    controller: UniversalController = Depends(get_controller)
):
    """
    Deletes an existing movement by its ID.
    If the movement does not exist, it returns a 404 error.
    """
    try:
        # Look for the movement to delete
        existing = controller.get_by_id(MovementOut, id)  # We use MovementOut for looking up the movement
        if not existing:
            raise HTTPException(404, detail="Movement not found")
        
        # Use the controller to delete the movement
        controller.delete(existing)
        
        return {
            "operation": "delete",
            "success": True,
            "message": f"Movement {id} deleted successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, detail=str(e))  # General server error