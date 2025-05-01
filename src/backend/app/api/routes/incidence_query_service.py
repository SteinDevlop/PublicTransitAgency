from fastapi import FastAPI, Form, Request, HTTPException, APIRouter, Query
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from backend.app.models.incidence import Incidence
from backend.app.logic.universal_controller_sql import UniversalController
from typing import List, Optional

app = APIRouter(prefix="/incidences", tags=["incidences"])
controller = UniversalController()
templates = Jinja2Templates(directory="src/backend/app/templates")  # Asegúrate de que la ruta sea correcta


@app.get("/", response_class=HTMLResponse)
def listar_incidencias(request: Request):
    """Renders the 'ListarIncidencia.html' template with all incidences."""
    incidences = controller.read_all(Incidence())
    return templates.TemplateResponse("ListarIncidencia.html", {"request": request, "incidences": incidences})


@app.get("/{incidence_id}", response_class=HTMLResponse)
def detalle_incidencia(incidence_id: int, request: Request):
    """Renders the 'DetalleIncidencia.html' template for a specific incidence."""
    incidence = controller.get_by_id(Incidence, incidence_id)
    if not incidence:
        raise HTTPException(status_code=404, detail="Incidence not found")
    return templates.TemplateResponse("DetalleIncidencia.html", {"request": request, "incidence": incidence})
