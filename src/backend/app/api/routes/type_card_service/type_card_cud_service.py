import logging
from fastapi import APIRouter, Form, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from backend.app.models.type_card import TypeCardOut, TypeCardCreate
from backend.app.logic.universal_controller_sqlserver import UniversalController
from backend.app.core.auth import get_current_user
from fastapi import Security

# Initialize the controller for type card
controller = UniversalController()

# Set up the template directory for rendering HTML
templates = Jinja2Templates(directory="src/backend/app/templates")

# Create a router for type card-related endpoints
app = APIRouter(prefix="/typecard", tags=["Type Card"])

# Set up logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Route to create a new type of card
@app.get("/crear", response_class=HTMLResponse)
def create_typecard_form(request: Request, current_user: dict = Security(get_current_user, scopes=["system", "administrador"])):
    """
    Displays the form to create a new type of card.
    """
    logger.info(f"[GET /crear] User {current_user['user_id']} accessed the create card type form.")
    return templates.TemplateResponse(request,"CrearTipoTarjeta.html", {"request": request})


# Route to delete an existing type of card
@app.get("/eliminar", response_class=HTMLResponse)
def delete_typecard_form(request: Request, current_user: dict = Security(get_current_user, scopes=["system", "administrador"])):
    """
    Displays the form to delete a type of card.
    """
    logger.info(f"[GET /eliminar] User {current_user['user_id']} accessed the delete card type form.")
    return templates.TemplateResponse(request,"EliminarTipoTarjeta.html", {"request": request})


# Route to update an existing type of card
@app.get("/actualizar", response_class=HTMLResponse)
def update_typecard_form(request: Request, current_user: dict = Security(get_current_user, scopes=["system", "administrador"])):
    """
    Displays the form to update an existing type of card.
    """
    logger.info(f"[GET /actualizar] User {current_user['user_id']} accessed the update card type form.")
    return templates.TemplateResponse(request,"ActualizarTipoTarjeta.html", {"request": request})


# Route to create a new type of card via POST
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

        logger.info(f"[POST /create] User {current_user['user_id']} created a new card type with ID {new_typecard.id} and type '{new_typecard.type}'.")

        return {
            "operation": "create",
            "success": True,
            "data": TypeCardOut(id=new_typecard.id, type=new_typecard.type).model_dump(),
            "message": "Card type created successfully"
        }
    except ValueError as e:
        logger.error(f"[POST /create] Error creating card type: {str(e)}")
        raise HTTPException(400, detail=str(e))  # Bad request if validation fails
    except Exception as e:
        logger.error(f"[POST /create] Internal server error: {str(e)}")
        raise HTTPException(500, detail=f"Internal server error: {str(e)}")  # General server error


# Route to update an existing type of card via POST
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
            logger.warning(f"[POST /update] Card type with ID {id} not found.")
            raise HTTPException(404, detail="Card type not found")

        # Create a new instance with the updated data
        updated_typecard = TypeCardCreate(id=id, type=type)

        # Update the type of card using the controller
        controller.update(updated_typecard)

        logger.info(f"[POST /update] User {current_user['user_id']} updated card type {id} to type '{updated_typecard.type}'.")

        return {
            "operation": "update",
            "success": True,
            "data": TypeCardOut(id=updated_typecard.id, type=updated_typecard.type).model_dump(),
            "message": f"Card type {id} updated successfully"
        }
    except ValueError as e:
        logger.error(f"[POST /update] Error updating card type: {str(e)}")
        raise HTTPException(400, detail=str(e))


# Route to delete an existing type of card via POST
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
            logger.warning(f"[POST /delete] Card type with ID {id} not found.")
            raise HTTPException(404, detail="Card type not found")

        # Delete the type of card using the controller
        controller.delete(existing)

        logger.info(f"[POST /delete] User {current_user['user_id']} deleted card type with ID {id}.")

        return {
            "operation": "delete",
            "success": True,
            "message": f"Card type {id} deleted successfully"
        }
    except HTTPException:
        raise  # Re-raise HTTPException as it is
    except Exception as e:
        logger.error(f"[POST /delete] Internal server error: {str(e)}")
        raise HTTPException(500, detail=str(e))
