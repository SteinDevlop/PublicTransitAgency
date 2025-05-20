import logging
from fastapi import APIRouter, HTTPException, Request, Security
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from backend.app.logic.universal_controller_instance import universal_controller as controller
from backend.app.models.routes import Route
from backend.app.core.auth import get_current_user

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

app = APIRouter(prefix="/routes", tags=["routes"])
templates = Jinja2Templates(directory="src/backend/app/templates")

@app.get("/", response_class=HTMLResponse)
def listar_rutas(
    request: Request,
    #current_user: dict = Security(get_current_user, scopes=["system", "administrador", "planificador"])
):
    """
    Lista todas las rutas.
    """
    try:
        rutas = controller.read_all(Route)
        logger.info(f"[GET /routes/] Se listaron {len(rutas)} rutas.")
        return templates.TemplateResponse("ListarRutas.html", {"request": request, "rutas": rutas})
    except Exception as e:
        logger.error(f"[GET /routes/] Error al listar rutas: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/{ID}", response_class=HTMLResponse)
def detalle_ruta(
    ID: int,
    request: Request,
    #current_user: dict = Security(get_current_user, scopes=["system", "administrador", "planificador"])
):
    """
    Obtiene el detalle de una ruta por su ID.
    """
    try:
        ruta = controller.get_by_id(Route, ID)
        if not ruta:
            logger.warning(f"[GET /routes/{ID}] Ruta no encontrada.")
            raise HTTPException(status_code=404, detail="Ruta no encontrada")
        logger.info(f"[GET /routes/{ID}] Se consultó la ruta con ID={ID}.")
        return templates.TemplateResponse("DetalleRuta.html", {"request": request, "route": ruta.to_dict()})
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"[GET /routes/{ID}] Error al consultar ruta: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))