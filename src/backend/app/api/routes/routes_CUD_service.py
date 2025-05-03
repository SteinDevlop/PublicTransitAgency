from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from backend.app.logic.universal_controller_sql import UniversalController
from backend.app.models.routes import Route

app = APIRouter(prefix="/routes", tags=["routes"])
controller = UniversalController()
templates = Jinja2Templates(directory="src/backend/app/templates")

@app.get("/create", response_class=HTMLResponse)
def crear_ruta_form(request: Request):
    return templates.TemplateResponse("CrearRuta.html", {"request": request})

@app.post("/create")
def crear_ruta(ID: int = Form(...), IDHorario: int = Form(...), Nombre: str = Form(...)):
    ruta = Route(ID=ID, IDHorario=IDHorario, Nombre=Nombre)
    try:
        controller.add(ruta)
        return {
            "operation": "create",
            "success": True,
            "data": ruta,
            "message": "Ruta creada exitosamente."
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/update", response_class=HTMLResponse)
def actualizar_ruta_form(request: Request):
    return templates.TemplateResponse("ActualizarRuta.html", {"request": request})

@app.post("/update")
def actualizar_ruta(ID: int = Form(...), IDHorario: int = Form(...), Nombre: str = Form(...)):
    ruta = Route(ID=ID, IDHorario=IDHorario, Nombre=Nombre)
    try:
        controller.update(ruta)
        return {
            "operation": "update",
            "success": True,
            "data": ruta,
            "message": "Ruta actualizada exitosamente."
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/delete", response_class=HTMLResponse)
def eliminar_ruta_form(request: Request):
    return templates.TemplateResponse("EliminarRuta.html", {"request": request})

@app.post("/delete")
def eliminar_ruta(ID: int = Form(...)):
    ruta = Route(ID=ID)
    try:
        controller.delete(ruta)
        return {
            "operation": "delete",
            "success": True,
            "message": "Ruta eliminada exitosamente."
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))