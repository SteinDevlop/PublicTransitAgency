from fastapi import FastAPI, Form, Request, HTTPException, APIRouter, Query
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from backend.app.models.maintainance_status import MaintainanceStatus
from backend.app.logic.universal_controller_sql import UniversalController

app = APIRouter(prefix="/maintainance-status", tags=["maintainance-status"])
controller = UniversalController()
templates = Jinja2Templates(directory="src/backend/app/templates")

@app.get("/", response_class=HTMLResponse)
def listar_estados(request: Request):
    """Renders the 'ListarMaintainanceStatus.html' template with all maintainance statuses."""
    estados = controller.read_all(MaintainanceStatus(status=""))
    return templates.TemplateResponse("ListarMaintainanceStatus.html", {"request": request, "estados": estados})

@app.get("/{id}", response_class=HTMLResponse)
def detalle_estado(id: int, request: Request):
    """Renders the 'DetalleMaintainanceStatus.html' template for a specific maintainance status."""
    estado = controller.get_by_id(MaintainanceStatus, id)
    if not estado:
        raise HTTPException(status_code=404, detail="Estado de mantenimiento no encontrado")
    return templates.TemplateResponse("DetalleMaintainanceStatus.html", {"request": request, "estado": estado})
