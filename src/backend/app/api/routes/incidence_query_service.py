from fastapi import FastAPI, Form, Request, HTTPException, APIRouter, Query
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from backend.app.models.incidence import IncidenceOut
from backend.app.logic.universal_controller_sql import UniversalController
from typing import List, Optional

app = APIRouter(prefix="/incidence", tags=["incidence"])
controller = UniversalController()
templates = Jinja2Templates(directory="src/backend/app/templates")  # Asegúrate de que la ruta sea correcta


@app.get('/consultar', response_class=HTMLResponse)
def consultar(request: Request):
    """Renders the 'ConsultarIncidencia.html' template."""
    return templates.TemplateResponse("ConsultarIncidencia.html", {"request": request})



@app.get("/incidencias", response_model=List[IncidenceOut])
async def get_all_incidences(
        status: Optional[str] = Query(None),
        skip: int = Query(0, ge=0),
        limit: int = Query(10, ge=1)
):
    """Retrieves all incidences from the database."""
    filters = {"status": status} if status else {}
    incidences = controller.read_all(IncidenceOut, filters=filters, skip=skip, limit=limit)
    return incidences #changed to return incidences



@app.get("/incidencia/{IncidenciaID}", response_class=HTMLResponse)
async def get_incidence_by_id(request: Request, IncidenciaID: int):
    """Retrieves an incidence by its ID and renders it using a template."""
    incidence = controller.get_by_id(IncidenceOut, IncidenciaID)
    if not incidence:
        raise HTTPException(status_code=404, detail="Incidencia not found")  # Devuelve 404 si no se encuentra
    return templates.TemplateResponse("incidencia.html", {
        "request": request,
        "IncidenciaID": incidence.IncidenciaID,
        "Descripcion": incidence.Descripcion,
        "Tipo": incidence.Tipo,
        "TicketID": incidence.TicketID
    })
