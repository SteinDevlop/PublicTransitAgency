from fastapi import APIRouter, HTTPException, Request, Security
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from backend.app.logic.universal_controller_sqlserver import UniversalController
from backend.app.models.routes import Route
from backend.app.core.auth import get_current_user

app = APIRouter(prefix="/routes", tags=["routes"])
controller = UniversalController()
templates = Jinja2Templates(directory="src/backend/app/templates")

@app.get("/", response_class=HTMLResponse)
def listar_rutas(
    request: Request,
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "planificador", "operador"])
):
    """
    Lista todas las rutas.
    """
    try:
        rutas = controller.read_all(Route)
        return templates.TemplateResponse("ListarRutas.html", {"request": request, "routes": rutas})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al listar las rutas: {str(e)}")

@app.get("/{ID}", response_class=HTMLResponse)
def detalle_ruta(
    ID: int,
    request: Request,
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "planificador", "operador"])
):
    """
    Muestra el detalle de una ruta específica por ID.
    """
    try:
        ruta = controller.get_by_id(Route, ID)
        if not ruta:
            raise HTTPException(status_code=404, detail="Ruta no encontrada")
        return templates.TemplateResponse("DetalleRuta.html", {"request": request, "route": ruta.to_dict()})
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener el detalle de la ruta: {str(e)}")
