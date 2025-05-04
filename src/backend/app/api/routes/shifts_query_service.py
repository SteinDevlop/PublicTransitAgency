from fastapi import APIRouter, HTTPException, Request, Security
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from backend.app.logic.universal_controller_sql import UniversalController
from backend.app.models.shift import Shift
from backend.app.core.auth import get_current_user  # Import for authentication

app = APIRouter(prefix="/shifts", tags=["shifts"])
controller = UniversalController()
templates = Jinja2Templates(directory="src/backend/app/templates")

@app.get("/", response_class=HTMLResponse)
def listar_turnos(
    request: Request,
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "supervisor"])
):
    """
    List all shifts. Requires authentication.
    """
    turnos = controller.read_all(Shift)
    return templates.TemplateResponse("ListarTurno.html", {"request": request, "shifts": turnos})

@app.get("/{ID}", response_class=HTMLResponse)
def detalle_turno(
    ID: int,
    request: Request,
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "supervisor"])
):
    """
    Get details of a specific shift by ID. Requires authentication.
    """
    turno = controller.get_by_id(Shift, ID)
    if not turno:
        raise HTTPException(status_code=404, detail="Turno no encontrado")
    return templates.TemplateResponse("DetalleTurno.html", {"request": request, "shift": turno})