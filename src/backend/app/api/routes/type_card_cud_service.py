from fastapi import APIRouter, Form, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from backend.app.models.type_card import TypeCardOut, TypeCardCreate
from backend.app.logic.universal_controller_sql import UniversalController

app = APIRouter(prefix="/typecard", tags=["Type Card"])
controller = UniversalController()  # Ensure the controller is correctly instantiated
templates = Jinja2Templates(directory="src/backend/app/templates")  # Set up the template directory

@app.get("/crear", response_class=HTMLResponse)
def crear_tipo_tarjeta(request: Request):
    """
    Displays the form to create a new type of card.
    """
    return templates.TemplateResponse("CrearTipoTarjeta.html", {"request": request})

# Route to delete a type of card
@app.get("/eliminar", response_class=HTMLResponse)
def eliminar_tipo_tarjeta(request: Request):
    """
    Displays the form to delete a type of card.
    """
    return templates.TemplateResponse("EliminarTipoTarjeta.html", {"request": request})

# Route to update a type of card
@app.get("/actualizar", response_class=HTMLResponse)
def actualizar_tipo_tarjeta(request: Request):
    """
    Displays the form to update an existing type of card.
    """
    return templates.TemplateResponse("ActualizarTipoTarjeta.html", {"request": request})

# Route to add a new type of card
@app.post("/create")
async def add_typecard(
    id: int = Form(...),
    type: str = Form(...),
):
    """
    Creates a new type of card with the provided ID and type.
    The controller is used to add the type of card to the database.
    """
    try:
        new_typecard = TypeCardCreate(id=id, type=type)
        
        # Add the new type of card using the controller
        result = controller.add(new_typecard)
        
        return {
            "operation": "create",
            "success": True,
            "data": TypeCardOut(id=new_typecard.id, type=new_typecard.type).model_dump(),
            "message": "Card type created successfully"
        }
    except ValueError as e:
        raise HTTPException(400, detail=str(e))  # Bad request if validation fails
    except Exception as e:
        raise HTTPException(500, detail=f"Internal server error: {str(e)}")  # General server error

# Route to update an existing type of card
@app.post("/update")
async def update_typecard(
    id: int = Form(...),
    type: str = Form(...),
):
    """
    Updates an existing type of card by its ID and new type.
    If the type of card does not exist, a 404 error is raised.
    """
    try:
        # Look for the existing type of card to update
        existing = controller.get_by_id(TypeCardOut, id)
        if not existing:
            raise HTTPException(404, detail="Card type not found")
        
        # Create a new instance with the updated data
        updated_typecard = TypeCardCreate(id=id, type=type)
        
        # Update the type of card using the controller
        result = controller.update(updated_typecard)
        
        return {
            "operation": "update",
            "success": True,
            "data": TypeCardOut(id=updated_typecard.id, type=updated_typecard.type).model_dump(),
            "message": f"Card type {id} updated successfully"
        }
    except ValueError as e:
        raise HTTPException(400, detail=str(e))  # Bad request if validation fails

# Route to delete a type of card
@app.post("/delete")
async def delete_typecard(id: int = Form(...)):
    """
    Deletes an existing type of card by its ID.
    If the type of card does not exist, a 404 error is raised.
    """
    try:
        existing = controller.get_by_id(TypeCardOut, id)
        if not existing:
            raise HTTPException(404, detail="Card type not found")

        controller.delete(existing)

        return {
            "operation": "delete",
            "success": True,
            "message": f"Card type {id} deleted successfully"
        }
    except HTTPException:
        raise  # ⚡ Deja pasar HTTPException tal como está
    except Exception as e:
        raise HTTPException(500, detail=str(e))  # Solo otros errores son 500

