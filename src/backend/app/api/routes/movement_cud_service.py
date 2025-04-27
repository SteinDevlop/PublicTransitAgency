from fastapi import FastAPI, Form, HTTPException, APIRouter, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from backend.app.models.movement import MovementCreate, MovementOut  # Make sure your models are in this file
from backend.app.logic.universal_controller_sql import UniversalController 
import uvicorn

app = APIRouter(prefix="/movement", tags=["movement"])  # Initialize the API router with the given prefix and tags
controller = UniversalController()  # Ensure the controller is correctly instantiated
templates = Jinja2Templates(directory="src/backend/app/templates")  # Set up the template directory

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
            "data": MovementOut(id=new_movement.id, tipo=new_movement.type, amount=new_movement.amount).dict(),
            "message": "Card created successfully"
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
):
    """
    Updates an existing card by its ID and new type.
    If the card does not exist, it returns a 404 error.
    """
    try:
        # Look for the existing movement to update
        existing = controller.get_by_id(MovementOut, id)  # We use MovementOut for looking up the card
        if not existing:
            raise HTTPException(404, detail="Card not found")
        
        # Create a CardCreate instance to validate the update data
        updated_card = CardCreate(
            id=id,
            tipo=tipo,
            saldo=existing.balance
        )
        # Use the controller to update the card (convert model to dict)
        result = controller.update(updated_card)
        
        # Return the updated card response using CardOut
        return {
            "operation": "update",
            "success": True,
            "data": CardOut(id=updated_card.id, tipo=updated_card.tipo, balance=updated_card.balance).dict(),
            "message": f"Card {id} updated successfully"
        }
    except ValueError as e:
        raise HTTPException(400, detail=str(e))  # Bad request if validation fails

# Route to delete a card by its ID
@app.post("/delete")
async def delete_card(id: int = Form(...)):
    """
    Deletes an existing card by its ID.
    If the card does not exist, it returns a 404 error.
    """
    try:
        # Look for the card to delete
        existing = controller.get_by_id(CardOut, id)  # We use CardOut for looking up the card
        if not existing:
            raise HTTPException(404, detail="Card not found")
        
        # Use the controller to delete the card
        controller.delete(existing)
        
        return {
            "operation": "delete",
            "success": True,
            "message": f"Card {id} deleted successfully"
        }
    except Exception as e:
        raise HTTPException(500, detail=str(e))  # General server error
