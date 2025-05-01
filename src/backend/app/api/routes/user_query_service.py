from fastapi import FastAPI, HTTPException, APIRouter, Form, Request, status, Query
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from backend.app.models.user import UserCreate, UserOut
from backend.app.logic.universal_controller_sql import UniversalController

# Initialize the controller to handle database operations
controller = UniversalController()
app = APIRouter(prefix="/user", tags=["user"])

# Route to get all the users from the database
@app.get("/users")
async def get_all():
    """
    Returns all the user records from the database.
    """
    return controller.read_all(UserOut)

# Route to view a specific user by its ID and render the 'usuario.html' template
@app.get("/{id}")
def get_by_id(id: int):
    """
    Fetches a card by its ID and renders its details on 'user.html'.
    If no user is found, returns 'None' for the details.
    """
    result = controller.get_by_id(UserOut, id)
    if not result:
        raise HTTPException(status_code=404, detail="Not found")
    return result.to_dict()
