from fastapi import FastAPI, Form, Request, status, Query, APIRouter
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from backend.app.core.auth import get_current_user, verify_role
from fastapi import Security
from backend.app.models.card import CardCreate, CardOut
from backend.app.logic.universal_controller_sql import UniversalController

# Initialize the FastAPI router for the "card" functionality
app = APIRouter(prefix="/card", tags=["card"])

# Initialize the controller to handle database operations
controller = UniversalController()

templates = Jinja2Templates(directory="src/backend/app/templates")

# Route to consult and display the 'ConsultarTarjeta' HTML page
@app.get('/consultar', response_class=HTMLResponse)
def consultar(request: Request,current_user: dict = Security(get_current_user, scopes=["system","administrador","pasajero","supervisor","mantenimiento"])):
    """
    Renders the 'ConsultarTarjeta.html' template to show the card consultation page.
    """
    return templates.TemplateResponse(request,"ConsultarTarjeta.html", {"request": request})

# Route to get all the cards from the database
@app.get("/tarjetas")
async def get_tarjetas(current_user: dict = Security(get_current_user, scopes=["system","administrador"])):
    """
    Returns all the card records from the database.
    """
    return controller.read_all(CardOut)

# Route to view a specific card by its ID and render the 'tarjeta.html' template
@app.get("/tarjeta", response_class=HTMLResponse)
def tarjeta(request: Request, id: int = Query(...),current_user: dict = Security(get_current_user, scopes=["system","administrador","pasajero"])):
    """
    Fetches a card by its ID and renders its details on 'tarjeta.html'.
    If no card is found, returns 'None' for the details.
    """
    unit_tarjeta = controller.get_by_id(CardOut, id)
    
    if unit_tarjeta:
        # If the card is found, display its details
        return templates.TemplateResponse(request,"tarjeta.html", {
            "request": request,
            "id": unit_tarjeta.id,
            "tipo": unit_tarjeta.tipo,
            "saldo": unit_tarjeta.balance
        })
    
    # If no card is found, display placeholders for the card details
    return templates.TemplateResponse(request,"tarjeta.html", {
        "request": request,
        "id": "None",
        "tipo": "None",
        "saldo": "None"
    })
