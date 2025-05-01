"""from fastapi import APIRouter, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from backend.app.logic.universal_controller_sql import UniversalController
from backend.app.models.incidence import Incidence

app = APIRouter(prefix="/incidence", tags=["incidence"])
controller = UniversalController()
templates = Jinja2Templates(directory="src/backend/app/templates")

@app.get("/create", response_class=HTMLResponse)
def crear_incidencia_form(request):
    return templates.TemplateResponse("CrearIncidencia.html", {"request": request})

@app.post("/create")
def crear_incidencia(description: str = Form(...), status: str = Form(...), type: str = Form(...)):
    incidencia = Incidence(description=description, status=status, type=type)
    try:
        controller.add(incidencia)
        return RedirectResponse("/incidences", status_code=303)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/update", response_class=HTMLResponse)
def actualizar_incidencia_form(request):
    return templates.TemplateResponse("ActualizarIncidencia.html", {"request": request})

@app.post("/update")
def actualizar_incidencia(incidence_id: int = Form(...), description: str = Form(...), status: str = Form(...), type: str = Form(...)):
    incidencia = Incidence(incidence_id=incidence_id, description=description, status=status, type=type)
    try:
        controller.update(incidencia)
        return RedirectResponse("/incidences", status_code=303)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/delete", response_class=HTMLResponse)
def eliminar_incidencia_form(request):
    return templates.TemplateResponse("EliminarIncidencia.html", {"request": request})

@app.post("/delete")
def eliminar_incidencia(incidence_id: int = Form(...)):
    incidencia = Incidence(incidence_id=incidence_id, description="", status="", type="")
    try:
        controller.delete(incidencia)
        return RedirectResponse("/incidences", status_code=303)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)
        """ 