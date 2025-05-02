from fastapi import FastAPI, Form, HTTPException, APIRouter, Request,Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from backend.app.models.card import CardCreate, CardOut  # Make sure your models are in this file
from backend.app.logic.universal_controller_sql import UniversalController 
from backend.app.core.auth import get_current_user, verify_role
from fastapi import Security

app = APIRouter(prefix="/card", tags=["card"])  # Initialize the API router with the given prefix and tags
controller = UniversalController()  # Ensure the controller is correctly instantiated
templates = Jinja2Templates(directory="src/backend/app/templates")  # Set up the template directory

# Route to display the "Create Card" form
@app.get("/crear", response_class=HTMLResponse)
def index_create(request: Request,current_user: dict = Security(get_current_user, scopes=["system","administrador","pasajero","supervisor","mantenimiento"])):
    """ 
    Displays the form to create a new card.
    """
    return templates.TemplateResponse(request, "CrearTarjeta.html", {"request": request})

# Route to display the "Update Card" form
@app.get("/actualizar", response_class=HTMLResponse)
def index_update(request: Request,current_user: dict = Security(get_current_user, scopes=["system","administrador"])):
    """
    Displays the form to update an existing card.
    """
    return templates.TemplateResponse(request, "ActualizarTarjeta.html", {"request": request})

# Route to display the "Delete Card" form
@app.get("/eliminar", response_class=HTMLResponse)
def index_delete(request: Request,current_user: dict = Security(get_current_user, scopes=["system","administrador"])):
    """
    Displays the form to delete an existing card.
    """
    return templates.TemplateResponse(request, "EliminarTarjeta.html", {"request": request})

# Route to create a new card
@app.post("/create")
async def create_card(
    id: int = Form(...),
    tipo: str = Form(...),current_user: dict = Security(get_current_user, scopes=["system","administrador","pasajero"])
):
    """
    Creates a new card with the provided ID and type. The balance is initialized to 0.
    """
    try:
        new_card = CardCreate(
            id=id,
            tipo=tipo,
            balance=0
        )
        # Do not call to_dict() here
        controller.add(new_card)
        
        return {
            "operation": "create",
            "success": True,
            "data": CardOut(id=new_card.id, tipo=new_card.tipo, balance=new_card.balance).model_dump(),
            "message": "Card created successfully"
        }
    except ValueError as e:
        raise HTTPException(400, detail=str(e))  # Bad request if validation fails
    except Exception as e:
        raise HTTPException(500, detail=f"Internal server error: {str(e)}")  # General server error

# Route to update an existing card
@app.post("/update")
async def update_card(
    id: int = Form(...),
    tipo: str = Form(...),current_user: dict = Security(get_current_user, scopes=["system","administrador"])
): 
    """
    Updates an existing card by its ID and new type.
    If the card does not exist, it returns a 404 error.
    """
    try:
        # Look for the existing card to update
        existing = controller.get_by_id(CardOut, id)  # We use CardOut for looking up the card
        if not existing:
            raise HTTPException(404, detail="Card not found")
        
        # Create a CardCreate instance to validate the update data
        updated_card = CardCreate(
            id=id,
            tipo=tipo,
            saldo=existing.balance
        )
        # Use the controller to update the card (convert model to dict)
        controller.update(updated_card)
        
        # Return the updated card response using CardOut
        return {
            "operation": "update",
            "success": True,
            "data": CardOut(id=updated_card.id, tipo=updated_card.tipo, balance=updated_card.balance).model_dump(),
            "message": f"Card {id} updated successfully"
        }
    except ValueError as e:
        raise HTTPException(400, detail=str(e))  # Bad request if validation fails

# Route to delete a card by its ID
@app.post("/delete")
async def delete_card(id: int = Form(...),current_user: dict = Security(get_current_user, scopes=["system","administrador"])):
    """
    Deletes an existing card by its ID.
    If the card does not exist, it returns a 404 error.
    """
    try:
        existing = controller.get_by_id(CardOut, id)
        if not existing:
            raise HTTPException(404, detail="Card not found")
        
        controller.delete(existing)
        
        return {
            "operation": "delete",
            "success": True,
            "message": f"Card {id} deleted successfully"
        }
    except HTTPException as e:
        raise e  # <<--- IMPORTANTE: Si ya es HTTPException, la dejamos pasar
    except Exception as e:
        raise HTTPException(500, detail=str(e))
