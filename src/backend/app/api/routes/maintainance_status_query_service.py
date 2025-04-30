from fastapi import FastAPI, Form, Request, HTTPException, APIRouter, Query
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from backend.app.models.maintainance_status import MaintainanceStatusOut
from backend.app.logic.universal_controller_sql import UniversalController

app = APIRouter(prefix="/maintainance_status", tags=["maintainance_status"])
controller = UniversalController()
templates = Jinja2Templates(directory="src/backend/app/templates")

@app.get('/consultar', response_class=HTMLResponse)
def consultar(request: Request):
    """Renders the 'ConsultarEstatusMantenimiento.html' template."""
    return templates.TemplateResponse("ConsultarEMantenimiento.html", {"request": request}) # Crear HTML

@app.get("/status")
async def get_all_status():
    """Retrieves all maintainance statuses from the database."""
    return controller.read_all(MaintainanceStatusOut)

@app.get("/status/{ID}", response_class=HTMLResponse) # Usar ID en la ruta
async def get_status_by_id(request: Request, ID: int):
    """Retrieves a maintainance status by its ID and renders it using a template."""
    status = controller.get_by_id(MaintainanceStatusOut, ID)
    if status:
        return templates.TemplateResponse("estatus.html", {  # Crear HTML
            "request": request,
            "ID": status.ID,
            "TipoEstado": status.TipoEstado,
            "UnidadTransporte": status.UnidadTransporte,
            "Status": status.Status
        })
    return templates.TemplateResponse("estatus.html", { # Crear HTML
        "request": request,
        "ID": "None",
        "TipoEstado": "None",
        "UnidadTransporte": "None",
        "Status": "None"
    })
