from fastapi import (
    Form, HTTPException, APIRouter, Request, Security
)
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from backend.app.models.card import CardCreate, CardOut
from backend.app.logic.universal_controller_sql import UniversalController
from backend.app.core.auth import get_current_user

# Create a router instance for all "/card" endpoints
app = APIRouter(prefix="/card", tags=["card"])

# Initialize the universal CRUD controller
controller = UniversalController()

# Configure Jinja2 template rendering
templates = Jinja2Templates(directory="src/backend/app/templates")


@app.get("/crear", response_class=HTMLResponse)
def index_create(
    request: Request,
    current_user: dict = Security(
        get_current_user,
        scopes=["system", "administrador", "pasajero", "supervisor", "mantenimiento"]
    )
):
    """
    Display the form to create a new card.
    """
    return templates.TemplateResponse("CrearTarjeta.html", {"request": request})


@app.get("/actualizar", response_class=HTMLResponse)
def index_update(
    request: Request,
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    """
    Display the form to update an existing card.
    """
    return templates.TemplateResponse("ActualizarTarjeta.html", {"request": request})


@app.get("/eliminar", response_class=HTMLResponse)
def index_delete(
    request: Request,
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    """
    Display the form to delete an existing card.
    """
    return templates.TemplateResponse("EliminarTarjeta.html", {"request": request})


@app.post("/create")
async def create_card(
    id: int = Form(...),
    tipo: str = Form(...),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "pasajero"])
):
    """
    Create a new card with the given ID and type.
    The balance is initialized to 0.
    """
    try:
        new_card = CardCreate(
            id=id,
            tipo=tipo,
            balance=0
        )

        controller.add(new_card)

        return {
            "operation": "create",
            "success": True,
            "data": CardOut(id=new_card.id, tipo=new_card.tipo, balance=new_card.balance).model_dump(),
            "message": "Card created successfully."
        }
    except ValueError as e:
        raise HTTPException(400, detail=str(e))
    except Exception as e:
        raise HTTPException(500, detail=f"Internal server error: {str(e)}")


@app.post("/update")
async def update_card(
    id: int = Form(...),
    tipo: str = Form(...),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    """
    Update an existing card by its ID and new type.
    Returns a 404 error if the card does not exist.
    """
    try:
        existing = controller.get_by_id(CardOut, id)
        if not existing:
            raise HTTPException(404, detail="Card not found")

        updated_card = CardCreate(
            id=id,
            tipo=tipo,
            balance=existing.balance
        )
        controller.update(updated_card)

        return {
            "operation": "update",
            "success": True,
            "data": CardOut(id=updated_card.id, tipo=updated_card.tipo, balance=updated_card.balance).model_dump(),
            "message": f"Card {id} updated successfully."
        }
    except ValueError as e:
        raise HTTPException(400, detail=str(e))
    except Exception as e:
        raise HTTPException(500, detail=f"Internal server error: {str(e)}")


@app.post("/delete")
async def delete_card(
    id: int = Form(...),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    """
    Delete an existing card by its ID.
    Returns a 404 error if the card does not exist.
    """
    try:
        existing = controller.get_by_id(CardOut, id)
        if not existing:
            raise HTTPException(404, detail="Card not found")

        controller.delete(existing)

        return {
            "operation": "delete",
            "success": True,
            "message": f"Card {id} deleted successfully."
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(500, detail=f"Internal server error: {str(e)}")
