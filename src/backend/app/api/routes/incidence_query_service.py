from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from backend.app.logic.universal_controller_sql import UniversalController
from backend.app.models.incidence import Incidence

app = APIRouter(prefix="/incidence", tags=["incidence"])
controller = UniversalController()
templates = Jinja2Templates(directory="src/backend/app/templates")

@app.get("/", response_class=HTMLResponse)
def listar_incidencias(request: Request):
    incidencias = controller.read_all(Incidence)
    return templates.TemplateResponse("ListarIncidencia.html", {"request": request, "incidencias": incidencias})

@app.get("/{ID}", response_class=HTMLResponse)
def detalle_incidencia(ID: int, request: Request):
    incidencia = controller.get_by_id(Incidence, ID)
    if not incidencia:
        raise HTTPException(status_code=404, detail="Incidencia no encontrada")
    return templates.TemplateResponse("DetalleIncidencia.html", {"request": request, "incidencia": incidencia})