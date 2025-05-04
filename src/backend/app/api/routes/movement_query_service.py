#movement_query_service.py
# # This file contains the query service for the Movement model using FastAPI.
# # It includes routes for retrieving all movements and fetching a specific movement by ID.

from fastapi import FastAPI, HTTPException, APIRouter, Form, Request, status, Query
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from backend.app.models.movement import MovementOut
from backend.app.logic.universal_controller_sql import UniversalController

# Initialize the controller to handle database operations
controller = UniversalController()
app = APIRouter(prefix="/movement", tags=["movement"])

# Route to get all the movement from the database
@app.get("/movements")
async def get_all():
    """
    Returns all the movement records from the database.
    """
    return controller.read_all(MovementOut)

# Route to view a specific user by its ID and render the 'movement.html' template
@app.get("/{id}")
def get_by_id(id: int):
    """
    Fetches a price by its ID and renders its details on 'precio.html'.
    If no price is found, returns 'None' for the details.
    """
    result = controller.get_by_id(MovementOut, id)
    if not result:
        raise HTTPException(status_code=404, detail="Not found")
    return result.to_dict()
