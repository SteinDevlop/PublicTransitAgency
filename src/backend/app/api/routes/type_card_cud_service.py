from fastapi import APIRouter, Form, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from backend.app.models.type_card import TypeCardOut, TypeCardCreate
from backend.app.logic.universal_controller_sql import UniversalController
from backend.app.core.auth import get_current_user
from fastapi import Security

# Create a router for type card-related endpoints
app = APIRouter(prefix="/typecard", tags=["Type Card"])

# Initialize the controller for type card
controller = UniversalController()

# Set up the template directory for rendering HTML
templates = Jinja2Templates(directory="src/backend/app/templates")


@app.get("/crear", response_class=HTMLResponse)
def create_typecard_form(request: Request, current_user: dict = Security(get_current_user, scopes=["system", "administrador"])):
    """
    Displays the form to create a new type of card.
    """
    return templates.TemplateResponse("CrearTipoTarjeta.html", {"request": request})


@app.get("/eliminar", response_class=HTMLResponse)
def delete_typecard_form(request: Request, current_user: dict = Security(get_current_user, scopes=["system", "administrador"])):
    """
    Displays the form to delete a type of card.
    """
    return templates.TemplateResponse("EliminarTipoTarjeta.html", {"request": request})


@app.get("/actualizar", response_class=HTMLResponse)
def update_typecard_form(request: Request, current_user: dict = Security(get_current_user, scopes=["system", "administrador"])):
    """
    Displays the form to update an existing type of card.
    """
    return templates.TemplateResponse("ActualizarTipoTarjeta.html", {"request": request})


@app.post("/create")
async def create_typecard(
    id: int = Form(...),
    type: str = Form(...),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    """
    Creates a new type of card with the provided ID and type.
    """
    try:
        new_typecard = TypeCardCreate(id=id, type=type)

        # Add the new type of card using the controller
        controller.add(new_typecard)

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


@app.post("/update")
async def update_typecard(
    id: int = Form(...),
    type: str = Form(...),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    """
    Updates an existing type of card by its ID and new type.
    If the type of card does not exist, a 404 error is raised.
    """
    try:
        # Check if the type of card exists
        existing = controller.get_by_id(TypeCardOut, id)
        if not existing:
            raise HTTPException(404, detail="Card type not found")

        # Create a new instance with the updated data
        updated_typecard = TypeCardCreate(id=id, type=type)

        # Update the type of card using the controller
        controller.update(updated_typecard)

        return {
            "operation": "update",
            "success": True,
            "data": TypeCardOut(id=updated_typecard.id, type=updated_typecard.type).model_dump(),
            "message": f"Card type {id} updated successfully"
        }
    except ValueError as e:
        raise HTTPException(400, detail=str(e))
    except Exception as e:
        raise HTTPException(500, detail=f"Internal server error: {str(e)}")


@app.post("/delete")
async def delete_typecard(
    id: int = Form(...),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    """
    Deletes an existing type of card by its ID.
    If the type of card does not exist, a 404 error is raised.
    """
    try:
        # Check if the type of card exists
        existing = controller.get_by_id(TypeCardOut, id)
        if not existing:
            raise HTTPException(404, detail="Card type not found")

        # Delete the type of card using the controller
        controller.delete(existing)

        return {
            "operation": "delete",
            "success": True,
            "message": f"Card type {id} deleted successfully"
        }
    except HTTPException:
        raise  # Re-raise HTTPException as it is
    except Exception as e:
        raise HTTPException(500, detail=str(e))
