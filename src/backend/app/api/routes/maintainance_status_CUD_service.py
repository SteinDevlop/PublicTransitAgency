from fastapi import FastAPI, Form, HTTPException, APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from backend.app.models.maintainance_status import MaintainanceStatusCreate, MaintainanceStatusOut, MaintainanceStatus
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

@app.get("/create", response_class=HTMLResponse)
def crear_estado_form(request: Request):
    """Renders the 'CrearMaintainanceStatus.html' template."""
    return templates.TemplateResponse("CrearMaintainanceStatus.html", {"request": request})

@app.post("/create")
def crear_estado(status: str = Form(...)):
    """Creates a new maintainance status."""
    estado = MaintainanceStatus(status=status)
    try:
        controller.add(estado)
        return RedirectResponse("/maintainance-status", status_code=303)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/update", response_class=HTMLResponse)
def actualizar_estado_form(request: Request):
    """Renders the 'ActualizarMaintainanceStatus.html' template."""
    return templates.TemplateResponse("ActualizarMaintainanceStatus.html", {"request": request})

@app.post("/update")
def actualizar_estado(id: int = Form(...), status: str = Form(...)):
    """Updates an existing maintainance status."""
    estado = MaintainanceStatus(id=id, status=status)
    try:
        controller.update(estado)
        return RedirectResponse("/maintainance-status", status_code=303)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/delete", response_class=HTMLResponse)
def eliminar_estado_form(request: Request):
    """Renders the 'EliminarMaintainanceStatus.html' template."""
    return templates.TemplateResponse("EliminarMaintainanceStatus.html", {"request": request})

@app.post("/delete")
def eliminar_estado(id: int = Form(...)):
    """Deletes an existing maintainance status."""
    estado = MaintainanceStatus(id=id, status="")
    try:
        controller.delete(estado)
        return RedirectResponse("/maintainance-status", status_code=303)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))