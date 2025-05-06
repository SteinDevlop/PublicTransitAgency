from fastapi import APIRouter, HTTPException, Request, Security
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from backend.app.logic.universal_controller_sql import UniversalController
from backend.app.models.routes import Route
from backend.app.core.auth import get_current_user  # Import for authentication

app = APIRouter(prefix="/routes", tags=["routes"])
controller = UniversalController()
templates = Jinja2Templates(directory="src/backend/app/templates")

@app.get("/list", response_class=HTMLResponse)
def listar_rutas(
    request: Request
    
):
    """
    List all routes. Requires authentication.
    """
    rutas = controller.read_all(Route)
    return templates.TemplateResponse("ListarRutas.html", {"request": request, "routes": rutas})

@app.get("/{ID}", response_class=HTMLResponse)
def detalle_ruta(
    ID: int,
    request: Request
    
):
    """
    Get details of a specific route by ID. Requires authentication.
    """
    ruta = controller.get_by_id(Route, ID)
    if not ruta:
        raise HTTPException(status_code=404, detail="Ruta no encontrada")
    return templates.TemplateResponse("DetalleRuta.html", {"request": request, "route": ruta})