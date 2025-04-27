from fastapi import FastAPI, Form, Request, status, Query, APIRouter
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from backend.app.models.movement import MovementCreate, MovementOut
from backend.app.logic.universal_controller_sql import UniversalController

# Initialize the FastAPI router for the "movement" functionality
app = APIRouter(prefix="/movement", tags=["movement"])

# Initialize the controller to handle database operations
controller = UniversalController()

templates = Jinja2Templates(directory="src/backend/app/templates")

# Route to consult and display the 'ConsultarMovimiento' HTML page
@app.get('/consultar', response_class=HTMLResponse)
def consultar(request: Request):
    """
    Renders the 'ConsultarMovimiento.html' template to show the movement consultation page.
    """
    return templates.TemplateResponse("ConsultarMovimiento.html", {"request": request})

# Route to get all the movements from the database
@app.get("/movimientos")
async def get_movimientos():
    """
    Returns all the movements records from the database.
    """
    return controller.read_all(MovementOut)

# Route to view a specific movimiento by its ID and render the 'movimiento.html' template
@app.get("/movimiento", response_class=HTMLResponse)
def movimiento(request: Request, id: int = Query(...)):
    """
    Fetches a movement by its ID and renders its details on 'movimiento.html'.
    If no movement is found, returns 'None' for the details.
    """
    unit_movement = controller.get_by_id(MovementOut, id)
    
    if unit_movement:
        # If the movement is found, display its details
        return templates.TemplateResponse("movimiento.html", {
            "request": request,
            "id": unit_movement.id,
            "tipo": unit_movement.type,
            "monto": unit_movement.amount
        })
    
    # If no movement is found, display placeholders for the movement details
    return templates.TemplateResponse("movimiento.html", {
        "request": request,
        "id": "None",
        "tipo": "None",
        "monto": "None"
    })
