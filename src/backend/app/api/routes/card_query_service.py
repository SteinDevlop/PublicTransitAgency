from fastapi import Request, Query, APIRouter, Security
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from backend.app.core.auth import get_current_user
from backend.app.models.card import CardOut
from backend.app.logic.universal_controller_sql import UniversalController

# Create the router for card-related endpoints
app = APIRouter(prefix="/card", tags=["card"])

# Initialize universal controller instance
controller = UniversalController()

# Setup Jinja2 template engine
templates = Jinja2Templates(directory="src/backend/app/templates")


@app.get("/consultar", response_class=HTMLResponse)
def consultar(
    request: Request,
    current_user: dict = Security(get_current_user, scopes=[
        "system", "administrador", "pasajero", "supervisor", "mantenimiento"
    ])
):
    """
    Render the 'ConsultarTarjeta.html' template for the card consultation page.
    """
    return templates.TemplateResponse("ConsultarTarjeta.html", {"request": request})


@app.get("/tarjetas")
async def get_tarjetas(
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    """
    Retrieve and return all card records from the database.
    """
    return controller.read_all(CardOut)


@app.get("/tarjeta", response_class=HTMLResponse)
def tarjeta(
    request: Request,
    id: int = Query(...),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "pasajero"])
):
    """
    Retrieve a card by its ID and render the 'tarjeta.html' template with its details.
    If the card is not found, display 'None' for all fields.
    """
    unit_tarjeta = controller.get_by_id(CardOut, id)

    context = {
        "request": request,
        "id": unit_tarjeta.id if unit_tarjeta else "None",
        "tipo": unit_tarjeta.tipo if unit_tarjeta else "None",
        "saldo": unit_tarjeta.balance if unit_tarjeta else "None"
    }

    return templates.TemplateResponse("tarjeta.html", context)
