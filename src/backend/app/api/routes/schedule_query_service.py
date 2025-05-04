from fastapi import APIRouter, HTTPException, Request, Security
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from backend.app.logic.universal_controller_sql import UniversalController
from backend.app.models.schedule import Schedule
from backend.app.core.auth import get_current_user  # Import for authentication

app = APIRouter(prefix="/schedules", tags=["schedules"])
controller = UniversalController()
templates = Jinja2Templates(directory="src/backend/app/templates")

@app.get("/", response_class=HTMLResponse)
def listar_horarios(
    request: Request,
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "supervisor"])
):
    """
    List all schedules. Requires authentication.
    """
    horarios = controller.read_all(Schedule)
    return templates.TemplateResponse("ListarHorarios.html", {"request": request, "horarios": horarios})

@app.get("/{ID}", response_class=HTMLResponse)
def detalle_horario(
    ID: int,
    request: Request,
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "supervisor"])
):
    """
    Get details of a specific schedule by ID. Requires authentication.
    """
    horario = controller.get_by_id(Schedule, ID)
    if not horario:
        raise HTTPException(status_code=404, detail="Horario no encontrado")
    return templates.TemplateResponse("DetalleHorario.html", {"request": request, "horario": horario})