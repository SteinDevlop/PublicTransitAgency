from fastapi import FastAPI, Form, Request, status, Query, APIRouter
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from backend.app.models.price import PriceCreate, PriceOut
from backend.app.logic.universal_controller_sql import UniversalController

# Initialize the FastAPI router for the "price" functionality
app = APIRouter(prefix="/price", tags=["price"])

# Initialize the controller to handle database operations
controller = UniversalController()

templates = Jinja2Templates(directory="src/backend/app/templates")

# Route to consult and display the 'ConsultarPrecio' HTML page
@app.get('/consultar', response_class=HTMLResponse)
def consultar(request: Request):
    """
    Renders the 'ConsultarPrecio.html' template to show the price consultation page.
    """
    return templates.TemplateResponse("ConsultarPrecio.html", {"request": request})

# Route to get all the prices from the database
@app.get("/precios")
async def get_precios():
    """
    Returns all the prices records from the database.
    """
    return controller.read_all(PriceOut)

# Route to view a specific prices by its ID and render the 'precio.html' template
@app.get("/precio", response_class=HTMLResponse)
def precio(request: Request, id: int = Query(...)):
    """
    Fetches a price by its ID and renders its details on 'precio.html'.
    If no price is found, returns 'None' for the details.
    """
    unit_price = controller.get_by_id(PriceOut, id)
    
    if unit_price:
        # If the price is found, display its details
        return templates.TemplateResponse("precio.html", {
            "request": request,
            "id": unit_price.id,
            "tipounidadtransporte": unit_price.unidadtransportype,
            "monto": unit_price.amount
        })
    
    # If no price is found, display placeholders for the price details
    return templates.TemplateResponse("precio.html", {
        "request": request,
        "id": "None",
        "tipounidadtransporte": "None",
        "monto": "None"
    })
