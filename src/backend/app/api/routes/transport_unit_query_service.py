from fastapi import APIRouter, HTTPException, Request, Security
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from backend.app.logic.universal_controller_sqlserver import UniversalController
from backend.app.models.transport import Transport
from backend.app.core.auth import get_current_user

app = APIRouter(prefix="/transports", tags=["transports"])
controller = UniversalController()
templates = Jinja2Templates(directory="src/backend/app/templates")

@app.get("/", response_class=HTMLResponse)
def listar_unidades(
    request: Request,
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "supervisor", "operador"])
):
    """
    Consulta la lista de todas las unidades de transporte.
    """
    try:
        unidades = controller.read_all(Transport)
        return templates.TemplateResponse("ListarTransports.html", {"request": request, "transports": unidades})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/{id}", response_class=HTMLResponse)
def detalle_unidad(
    id: int,
    request: Request,
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "supervisor", "operador"])
):
    """
    Consulta el detalle de una unidad de transporte específica por su ID.
    """
    try:
        unidad = controller.get_by_id(Transport, id)
        if not unidad:
            raise HTTPException(status_code=404, detail="Unidad de transporte no encontrada")
        return templates.TemplateResponse("DetalleTransport.html", {"request": request, "transport": unidad.to_dict()})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))