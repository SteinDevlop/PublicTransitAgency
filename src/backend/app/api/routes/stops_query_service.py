from fastapi import APIRouter, HTTPException, Request, Security
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from backend.app.logic.universal_controller_sql import UniversalController
from backend.app.models.stops import Stop
from backend.app.core.auth import get_current_user  # Import for authentication

app = APIRouter(prefix="/stops", tags=["stops"])
controller = UniversalController()
templates = Jinja2Templates(directory="src/backend/app/templates")

@app.get("/", response_class=HTMLResponse)
def listar_paradas(
    request: Request,
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "supervisor"])
):
    """
    List all stops. Requires authentication.
    """
    paradas = controller.read_all(Stop)
    return templates.TemplateResponse("ListarParadas.html", {"request": request, "paradas": paradas})

@app.get("/{ID}", response_class=HTMLResponse)
def detalle_parada(
    ID: int,
    request: Request,
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "supervisor"])
):
    """
    Get details of a specific stop by ID. Requires authentication.
    """
    parada = controller.get_by_id(Stop, ID)
    if not parada:
        raise HTTPException(status_code=404, detail="Parada no encontrada")
    return templates.TemplateResponse("DetalleParada.html", {"request": request, "parada": parada})