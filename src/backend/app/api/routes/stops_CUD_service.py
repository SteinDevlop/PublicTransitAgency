from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from backend.app.logic.universal_controller_sql import UniversalController
from backend.app.models.stops import Stop

app = APIRouter(prefix="/stops", tags=["stops"])
controller = UniversalController()
templates = Jinja2Templates(directory="src/backend/app/templates")

@app.get("/create", response_class=HTMLResponse)
def crear_parada_form(request: Request):
    return templates.TemplateResponse("CrearParada.html", {"request": request})

@app.post("/create")
def crear_parada(ID: int = Form(...), Nombre: str = Form(...), Ubicacion: str = Form(...)):
    parada = Stop(ID=ID, Nombre=Nombre, Ubicacion=Ubicacion)
    try:
        controller.add(parada)
        return {
            "operation": "create",
            "success": True,
            "data": parada,
            "message": "Parada creada exitosamente."
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/update", response_class=HTMLResponse)
def actualizar_parada_form(request: Request):
    return templates.TemplateResponse("ActualizarParada.html", {"request": request})

@app.post("/update")
def actualizar_parada(ID: int = Form(...), Nombre: str = Form(...), Ubicacion: str = Form(...)):
    parada = Stop(ID=ID, Nombre=Nombre, Ubicacion=Ubicacion)
    try:
        controller.update(parada)
        return {
            "operation": "update",
            "success": True,
            "data": parada,
            "message": "Parada actualizada exitosamente."
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/delete", response_class=HTMLResponse)
def eliminar_parada_form(request: Request):
    return templates.TemplateResponse("EliminarParada.html", {"request": request})

@app.post("/delete")
def eliminar_parada(ID: int = Form(...)):
    parada = Stop(ID=ID)
    try:
        controller.delete(parada)
        return {
            "operation": "delete",
            "success": True,
            "message": "Parada eliminada exitosamente."
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))