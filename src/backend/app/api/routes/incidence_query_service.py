from fastapi import FastAPI, Form, Request, HTTPException, APIRouter, Query
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from backend.app.models.incidence import IncidenceOut
from backend.app.logic.universal_controller_sql import UniversalController

app = APIRouter(prefix="/incidence", tags=["incidence"])
controller = UniversalController()
templates = Jinja2Templates(directory="src/backend/app/templates")

@app.get('/consultar', response_class=HTMLResponse)
def consultar(request: Request):
    """Renders the 'ConsultarIncidencia.html' template."""
    return templates.TemplateResponse("ConsultarIncidencia.html", {"request": request})

@app.get("/incidencias")
async def get_all_incidences():
    """Retrieves all incidences from the database."""
    return controller.read_all(IncidenceOut)

@app.get("/incidencia/{IncidenciaID}", response_class=HTMLResponse)
async def get_incidence_by_id(request: Request, IncidenciaID: int):
    """Retrieves an incidence by its ID and renders it using a template."""
    incidence = controller.get_by_id(IncidenceOut, IncidenciaID)
    if incidence:
        return templates.TemplateResponse("incidencia.html", {
            "request": request,
            "IncidenciaID": incidence.IncidenciaID,
            "Descripcion": incidence.Descripcion,
            "Tipo": incidence.Tipo,
            "TicketID": incidence.TicketID
        })
    return templates.TemplateResponse("incidencia.html", {
        "request": request,
        "IncidenciaID": "None",
        "Descripcion": "None",
        "Tipo": "None",
        "TicketID": "None"
    })