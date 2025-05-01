from fastapi import APIRouter, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from backend.app.logic.universal_controller_sql import UniversalController
from backend.app.models.transport import TransportUnitCreate

app = APIRouter(prefix="/transports", tags=["transports"])
controller = UniversalController()
templates = Jinja2Templates(directory="src/backend/app/templates")

@app.get("/create", response_class=HTMLResponse)
def crear_unidad_form(request):
    return templates.TemplateResponse("CrearTransport.html", {"request": request})

@app.post("/create")
def crear_unidad(id: str = Form(...), type: str = Form(...), status: str = Form(...), ubication: str = Form(...), capacity: int = Form(...)):
    unidad = TransportUnitCreate(id=id, type=type, status=status, ubication=ubication, capacity=capacity)
    try:
        controller.add(unidad)
        return RedirectResponse("/transports", status_code=303)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/update", response_class=HTMLResponse)
def actualizar_unidad_form(request):
    return templates.TemplateResponse("ActualizarTransport.html", {"request": request})

@app.post("/update")
def actualizar_unidad(id: str = Form(...), type: str = Form(...), status: str = Form(...), ubication: str = Form(...), capacity: int = Form(...)):
    unidad = TransportUnitCreate(id=id, type=type, status=status, ubication=ubication, capacity=capacity)
    try:
        controller.update(unidad)
        return RedirectResponse("/transports", status_code=303)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/delete", response_class=HTMLResponse)
def eliminar_unidad_form(request):
    return templates.TemplateResponse("EliminarTransport.html", {"request": request})

@app.post("/delete")
def eliminar_unidad(id: str = Form(...)):
    unidad = TransportUnitCreate(id=id, type="", status="", ubication="", capacity=0)
    try:
        controller.delete(unidad)
        return RedirectResponse("/transports", status_code=303)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))