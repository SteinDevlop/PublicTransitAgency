from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from backend.app.logic.universal_controller_sql import UniversalController
from backend.app.models.transport import Transport

app = APIRouter(prefix="/transports", tags=["transports"])
controller = UniversalController()
templates = Jinja2Templates(directory="src/backend/app/templates")

@app.get("/", response_class=HTMLResponse)
def listar_unidades(request: Request):
    unidades = controller.read_all(Transport)
    return templates.TemplateResponse(request,"ListarTransports.html", {"request": request, "transports": unidades})

@app.get("/{id}", response_class=HTMLResponse)
def detalle_unidad(id: int, request: Request):
    unidad = controller.get_by_id(Transport, id)
    if not unidad:
        raise HTTPException(status_code=404, detail="Unidad de transporte no encontrada")
    return templates.TemplateResponse(request,"DetalleTransport.html", {"request": request, "transports": [unidad]})