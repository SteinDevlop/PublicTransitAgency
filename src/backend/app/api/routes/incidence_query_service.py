from fastapi import FastAPI, Form, Request, HTTPException, APIRouter, Query
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
<<<<<<< HEAD
from backend.app.models.incidence import Incidence
=======
from backend.app.models.incidence import IncidenceOut
>>>>>>> d9ce6cb (Rewind)
from backend.app.logic.universal_controller_sql import UniversalController
from typing import List, Optional

app = APIRouter(prefix="/incidence", tags=["incidence"])
controller = UniversalController()
templates = Jinja2Templates(directory="src/backend/app/templates")  # Asegúrate de que la ruta sea correcta
<<<<<<< HEAD


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
=======


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
>>>>>>> d9ce6cb (Rewind)
