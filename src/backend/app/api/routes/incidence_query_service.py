from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from backend.app.logic.universal_controller_sql import UniversalController
from backend.app.models.incidence import IncidenceOut

app = APIRouter(prefix="/incidence", tags=["incidence"])
controller = UniversalController()
templates = Jinja2Templates(directory="src/backend/app/templates")

@app.get("/consultar", response_class=HTMLResponse)
def consultar_incidencias(request: Request):
    """Muestra la página para consultar incidencias."""
    incidencias = controller.read_all(IncidenceOut)
    return templates.TemplateResponse("ConsultarIncidencia.html", {"request": request, "incidencias": incidencias})

@app.get("/incidencia/{IncidenciaID}", response_model=IncidenceOut)
def obtener_incidencia(IncidenciaID: int):
    """Obtiene una incidencia por su ID."""
    incidencia = controller.get_by_id(IncidenceOut, IncidenciaID)
    if not incidencia:
        raise HTTPException(status_code=404, detail="Incidence not found")
    return incidencia