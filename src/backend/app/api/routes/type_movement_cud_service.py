from fastapi import APIRouter, Form, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from backend.app.models.type_movement import TypeMovementCreate, TypeMovementOut
from backend.app.logic.universal_controller_sql import UniversalController

app = APIRouter(prefix="/typemovement", tags=["Type Movement"])
controller = UniversalController()  # Ensure the controller is correctly instantiated
templates = Jinja2Templates(directory="src/backend/app/templates")  # Set up the template directory

@app.get("/crear", response_class=HTMLResponse)
def crear_tipo_movimiento(request: Request):
    """
    Displays the form to create a new type of movement.
    """
    return templates.TemplateResponse("CrearTipoMovimiento.html", {"request": request})

# Route to delete a type of movement
@app.get("/eliminar", response_class=HTMLResponse)
def eliminar_tipo_movimiento(request: Request):
    """
    Displays the form to delete a type of movement.
    """
    return templates.TemplateResponse("EliminarTipoMovimiento.html", {"request": request})

# Route to update a type of movement
@app.get("/actualizar", response_class=HTMLResponse)
def actualizar_tipo_movimiento(request: Request):
    """
    Displays the form to update an existing type of movement.
    """
    return templates.TemplateResponse("ActualizarTipoMovimiento.html", {"request": request})

# Route to add a new type of card
@app.post("/create")
async def add_typemovement(
    id: int = Form(...),
    type: str = Form(...),
):
    """
    Creates a new type of movement with the provided ID and type.
    The controller is used to add the type of movement to the database.
    """
    try:
        new_typecard = TypeMovementCreate(id=id, type=type)
        
        # Add the new type of card using the controller
        result = controller.add(new_typecard)
        
        return {
            "operation": "create",
            "success": True,
            "data": TypeMovementOut(id=new_typecard.id, type=new_typecard.type).dict(),
            "message": "Movement type created successfully"
        }
    except ValueError as e:
        raise HTTPException(400, detail=str(e))  # Bad request if validation fails
    except Exception as e:
        raise HTTPException(500, detail=f"Internal server error: {str(e)}")  # General server error

# Route to update an existing type of movement
@app.post("/update")
async def update_typemovement(
    id: int = Form(...),
    type: str = Form(...),
):
    """
    Updates an existing type of movement by its ID and new type.
    If the type of movement does not exist, a 404 error is raised.
    """
    try:
        # Look for the existing type of card to update
        existing = controller.get_by_id(TypeMovementOut, id)
        if not existing:
            raise HTTPException(404, detail="Movement type not found")
        
        # Create a new instance with the updated data
        updated_typemovement = TypeMovementCreate(id=id, type=type)
        
        # Update the type of movement using the controller
        result = controller.update(updated_typemovement)
        
        return {
            "operation": "update",
            "success": True,
            "data": TypeMovementOut(id=updated_typemovement.id, type=updated_typemovement.type).dict(),
            "message": f"Movement type {id} updated successfully"
        }
    except ValueError as e:
        raise HTTPException(400, detail=str(e))  # Bad request if validation fails

# Route to delete a type of movement
@app.post("/delete")
async def delete_typemovement(id: int = Form(...)):
    """
    Deletes an existing type of movement by its ID.
    If the type of movement does not exist, a 404 error is raised.
    """
    try:
        # Look for the type of movement to delete
        existing = controller.get_by_id(TypeMovementOut, id)
        if not existing:
            raise HTTPException(404, detail="Movement type not found")
        
        # Delete the type of movement using the controller
        controller.delete(existing)
        
        return {
            "operation": "delete",
            "success": True,
            "message": f"Movement type {id} deleted successfully"
        }
    except Exception as e:
        raise HTTPException(500, detail=str(e))  # General server error

