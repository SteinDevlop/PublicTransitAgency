import logging
import json
from fastapi import Request, Query, APIRouter, Security
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import HTTPException

from backend.app.core.auth import get_current_user
from backend.app.models.type_transport import TypeTransportOut
from backend.app.logic.universal_controller_instance import universal_controller as controller

# Configuración del logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Create the router for user-related endpoints
app = APIRouter(prefix="/typetransport", tags=["typetransport"])
# Initialize universal controller instance


# Setup Jinja2 template engine
templates = Jinja2Templates(directory="src/backend/app/templates")


@app.get("/consultar", response_class=HTMLResponse)
def consultar(
    request: Request,
    #current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    """
    Render the 'ConsultarTipoTransporte.html' template for the user consultation page.
    """
    #logger.info(f"[GET /consultar] Usuario: {current_user['user_ID']} - Mostrando página de consulta de tipo de transporte")
    return templates.TemplateResponse("ConsultarTipoTransporte.html", {"request": request})


@app.get("/typetransports")
async def get_typetransport(
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    """
    Retrieve and return all typetransports records from the database.
    """
    #logger.info(f"[GET /typetransports] Usuario: {current_user['user_ID']} - Consultando todas los tipos de transporte.")
    typetransports = controller.read_all(TypeTransportOut)
    logger.info(f"[GET /typetransports] Número de tipo de transportes encontrados: {len(typetransports)}")
    return typetransports


@app.get("/tipotransporte", response_class=HTMLResponse)
def typetransport(
    request: Request,
    id: int = Query(...),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    """
    Retrieve a user by its ID and render the 'typetransport.html' template with its details.
    If the user is not found, display 'None' for all fields.
    """
    #logger.info(f"[GET /typetransport] Usuario: {current_user['user_ID']} - Consultando tipo de transporte con ID={ID}")
    unit_typetransport= controller.get_by_column(TypeTransportOut, "ID",id)

    if not unit_typetransport:
        logger.warning(f"[GET /typetransport] No se encontró tipo de transporte con id={id}")
        raise HTTPException(status_code=404, detail="Tipo de transporte no encontrado")
        
    else:
        context = {
            "ID": unit_typetransport.ID if unit_typetransport else "None",
            "TipoTransporte": unit_typetransport.TipoTransporte if unit_typetransport else "None"
        }

        return templates.TemplateResponse(request, "tipotransporte.html", context)
