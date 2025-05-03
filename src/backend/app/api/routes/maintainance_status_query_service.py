from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from backend.app.logic.universal_controller_sql import UniversalController
from backend.app.models.maintainance_status import MaintainanceStatus

app = APIRouter(prefix="/maintainance_status", tags=["maintainance_status"])
controller = UniversalController()
templates = Jinja2Templates(directory="src/backend/app/templates")

@app.get("/", response_class=HTMLResponse)
def listar_estados(request: Request):
    estados = controller.read_all(MaintainanceStatus)
    return templates.TemplateResponse("ListaEstados.html", {"request": request, "estados": estados})

@app.get("/{id}", response_class=HTMLResponse)
def detalle_estado(id: int, request: Request):
    estado = controller.get_by_id(MaintainanceStatus, id)
    if not estado:
        raise HTTPException(status_code=404, detail="Estado de mantenimiento no encontrado")
    return templates.TemplateResponse("DetalleEMantenimiento.html", {"request": request, "data": estado})