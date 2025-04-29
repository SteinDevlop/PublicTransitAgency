from fastapi import FastAPI, Form, HTTPException, APIRouter, Request, Depends, status, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from backend.app.models.price import PriceCreate, PriceOut  # Make sure your models are in this file
from backend.app.logic.universal_controller_sql import UniversalController 
import uvicorn

app = APIRouter(prefix="/price", tags=["price"])  # Initialize the API router with the given prefix and tag
templates = Jinja2Templates(directory="src/backend/app/templates")  # Set up the template directory

def get_controller():
    """
    Dependency to get the controller instance.
    """
    return UniversalController()

# Route to display the "Create price" form
@app.get("/crear", response_class=HTMLResponse)
def index(request: Request):
    """
    Displays the form to create a new price.
    """
    return templates.TemplateResponse("CrearPrecio.html", {"request": request})

# Route to display the "Update price" form
@app.get("/actualizar", response_class=HTMLResponse)
def index(request: Request):
    """
    Displays the form to update an existing price.
    """
    return templates.TemplateResponse("ActualizarPrecio.html", {"request": request})

# Route to display the "Delete price" form
@app.get("/eliminar", response_class=HTMLResponse)
def index(request: Request):
    """
    Displays the form to delete an existing price.
    """
    return templates.TemplateResponse("EliminarPrecio.html", {"request": request})

# Route to create a new price
@app.post("/create")
async def create_price(
    id: int = Form(...),
    unidadtransportype: str = Form(...),
    amount: float = Form(...),
    controller: UniversalController = Depends(get_controller)
):
    """
    Creates a new price with the provided ID , type and amount.
    """
    try:
        new_price = PriceCreate(
            id=id,
            unidadtransportype=unidadtransportype,
            amount=amount,
        )
        # Do not call to_dict() here
        result = controller.add(new_price)
        
        return {
            "operation": "create",
            "success": True,
            "data": PriceOut(id=new_price.id, unidadtransportype=new_price.unidadtransportype, amount=new_price.amount).dict(),
            "message": "Price created successfully"
        }
    except ValueError as e:
        raise HTTPException(400, detail=str(e))  # Bad request if validation fails
    except Exception as e:
        raise HTTPException(500, detail=f"Internal server error: {str(e)}")  # General server error

# Route to update an existing price
@app.post("/update")
async def update_price(
    id: int = Form(...),
    unidadtransportype: str = Form(...),
    amount: float = Form(...),
    controller: UniversalController = Depends(get_controller)
):
    """
    Updates an existing price by its ID and new type.
    If the price does not exist, it returns a 404 error.
    """
    try:
        # Look for the existing price to update
        existing = controller.get_by_id(PriceOut, id)  # We use priceOut for looking up the price
        if not existing:
            raise HTTPException(404, detail="price not found")
        
        # Create a priceCreate instance to validate the update data
        updated_price = PriceCreate(
            id=id,
            unidadtransportype=unidadtransportype,
            amount=existing.amount
        )
        # Use the controller to update the price (convert model to dict)
        result = controller.update(updated_price)
        
        # Return the updated price response using priceOut
        return {
            "operation": "update",
            "success": True,
            "data": PriceOut(id=updated_price.id, unidadtransportype=updated_price.unidadtransportype, 
                             amount=updated_price.amount).dict(),
            "message": f"Price {id} updated successfully"
        }
    except ValueError as e:
        raise HTTPException(400, detail=str(e))  # Bad request if validation fails

# Route to delete a price by its ID
@app.post("/delete")
async def delete_price(
    id: int = Form(...),
    controller: UniversalController = Depends(get_controller)
):
    """
    Deletes an existing price by its ID.
    If the price does not exist, it returns a 404 error.
    """
    try:
        # Look for the price to delete
        existing = controller.get_by_id(PriceOut, id)  # We use PriceOut for looking up the price
        if not existing:
            raise HTTPException(404, detail="Price not found")
        
        # Use the controller to delete the price
        controller.delete(existing)
        
        return {
            "operation": "delete",
            "success": True,
            "message": f"price {id} deleted successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, detail=str(e))  # General server error