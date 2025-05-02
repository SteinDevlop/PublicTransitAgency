from fastapi import FastAPI, HTTPException, APIRouter, Form, Request, status, Query
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from backend.app.models.price import PriceCreate, PriceOut
from backend.app.logic.universal_controller_sql import UniversalController

# Initialize the controller to handle database operations
controller = UniversalController()
app = APIRouter(prefix="/price", tags=["price"])

# Route to get all the users from the database
@app.get("/prices")
async def get_all():
    """
    Returns all the price records from the database.
    """
    return controller.read_all(PriceOut)

# Route to view a specific user by its ID and render the 'precio.html' template
@app.get("/{id}")
def get_by_id(id: int):
    """
    Fetches a price by its ID and renders its details on 'precio.html'.
    If no price is found, returns 'None' for the details.
    """
    result = controller.get_by_id(PriceOut, id)
    if not result:
        raise HTTPException(status_code=404, detail="Not found")
    return result.to_dict()
