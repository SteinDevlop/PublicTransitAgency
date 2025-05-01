from fastapi import APIRouter, Form, HTTPException
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
def crear_incidencia(description: str = Form(...), type: str = Form(...), status: str = Form(...)):
    incidence = Incidence(description=description, type=type, status=status)
    controller.add(incidence)
    return RedirectResponse("/incidences/", status_code=303)


@app.get("/update", response_class=HTMLResponse)
def actualizar_incidencia_form(request):
    return templates.TemplateResponse("ActualizarIncidencia.html", {"request": request})


@app.post("/update")
def actualizar_incidencia(incidence_id: int = Form(...), description: str = Form(None), type: str = Form(None), status: str = Form(None)):
    incidence = controller.get_by_id(Incidence, incidence_id)
    if not incidence:
        raise HTTPException(status_code=404, detail="Incidence not found")
    updated_data = {"description": description, "type": type, "status": status}
    for key, value in updated_data.items():
        if value is not None:
            setattr(incidence, key, value)
    controller.update(incidence)
    return RedirectResponse("/incidences/", status_code=303)


@app.get("/delete", response_class=HTMLResponse)
def eliminar_incidencia_form(request):
    return templates.TemplateResponse("EliminarIncidencia.html", {"request": request})


@app.post("/delete")
def eliminar_incidencia(incidence_id: int = Form(...)):
    incidence = controller.get_by_id(Incidence, incidence_id)
    if not incidence:
        raise HTTPException(status_code=404, detail="Incidence not found")
    controller.delete(incidence)
    return RedirectResponse("/incidences/", status_code=303)
