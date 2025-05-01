"""from fastapi import FastAPI, Request, HTTPException, APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
<<<<<<< HEAD
from backend.app.models.incidence import Incidence
=======
from backend.app.models.incidence import IncidenceOut, Incidence
>>>>>>> e4587d1 (changes to incidence logic)
from backend.app.logic.universal_controller_sql import UniversalController

app = APIRouter(prefix="/incidences", tags=["incidences"])
controller = UniversalController()
templates = Jinja2Templates(directory="src/backend/app/templates")


@app.get("/", response_class=HTMLResponse)
def listar_incidencias(request: Request):
<<<<<<< HEAD
    |||Renders the 'ListarIncidencia.html' template with all incidences.|||
    incidencias = controller.read_all(Incidence(description="", status="", type=""))
=======
    """Renders the 'ListarIncidencia.html' template with all incidences."""
    incidencias = controller.read_all(Incidence(description="", type="", status=""))
>>>>>>> e4587d1 (changes to incidence logic)
    return templates.TemplateResponse("ListarIncidencia.html", {"request": request, "incidencias": incidencias})


@app.get("/{incidence_id}", response_class=HTMLResponse)
def detalle_incidencia(incidence_id: int, request: Request):
<<<<<<< HEAD
    |||Renders the 'DetalleIncidencia.html' template for a specific incidence.|||
=======
    """Renders the 'DetalleIncidencia.html' template for a specific incidence."""
>>>>>>> e4587d1 (changes to incidence logic)
    incidencia = controller.get_by_id(Incidence, incidence_id)
    if not incidencia:
        raise HTTPException(status_code=404, detail="Incidencia no encontrada")
    return templates.TemplateResponse("DetalleIncidencia.html", {"request": request, "incidencia": incidencia})
<<<<<<< HEAD
"""
=======
>>>>>>> e4587d1 (changes to incidence logic)
