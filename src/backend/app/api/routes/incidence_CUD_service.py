<<<<<<< HEAD
"""from fastapi import APIRouter, Form, HTTPException
=======
from fastapi import APIRouter, Form, HTTPException
>>>>>>> e4587d1 (changes to incidence logic)
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
<<<<<<< HEAD
def crear_incidencia(description: str = Form(...), status: str = Form(...), type: str = Form(...)):
    incidencia = Incidence(description=description, status=status, type=type)
=======
def crear_incidencia(description: str = Form(...), type: str = Form(...), status: str = Form(...)):
    incidencia = Incidence(description=description, type=type, status=status)
>>>>>>> e4587d1 (changes to incidence logic)
    try:
        controller.add(incidencia)
        return RedirectResponse("/incidences", status_code=303)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/update", response_class=HTMLResponse)
def actualizar_incidencia_form(request):
    return templates.TemplateResponse("ActualizarIncidencia.html", {"request": request})

@app.post("/update")
<<<<<<< HEAD
def actualizar_incidencia(incidence_id: int = Form(...), description: str = Form(...), status: str = Form(...), type: str = Form(...)):
    incidencia = Incidence(incidence_id=incidence_id, description=description, status=status, type=type)
=======
def actualizar_incidencia(incidence_id: int = Form(...), description: str = Form(...), type: str = Form(...), status: str = Form(...)):
    incidencia = Incidence(incidence_id=incidence_id, description=description, type=type, status=status)
>>>>>>> e4587d1 (changes to incidence logic)
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
<<<<<<< HEAD
    incidencia = Incidence(incidence_id=incidence_id, description="", status="", type="")
=======
    incidencia = Incidence(incidence_id=incidence_id, description="", type="", status="")
>>>>>>> e4587d1 (changes to incidence logic)
    try:
        controller.delete(incidencia)
        return RedirectResponse("/incidences", status_code=303)
    except ValueError as e:
<<<<<<< HEAD
        raise HTTPException(status_code=404, detail=str(e)
        """ 
=======
        raise HTTPException(status_code=404, detail=str(e))
>>>>>>> e4587d1 (changes to incidence logic)
