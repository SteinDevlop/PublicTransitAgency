from fastapi import APIRouter, Form, HTTPException, Security, Request
from backend.app.logic.universal_controller_sqlserver import UniversalController
from backend.app.models.transport import Transport
from backend.app.core.auth import get_current_user
from starlette.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = APIRouter(prefix="/transports", tags=["transports"])
controller = UniversalController()
templates = Jinja2Templates(directory="src/backend/app/templates")

@app.get("/create", response_class=HTMLResponse)
def crear_unidad_form(
    request: Request,
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "supervisor"])
):
    """
    Renderiza el formulario para crear una unidad de transporte.
    """
    return templates.TemplateResponse("CrearTransport.html", {"request": request})

@app.get("/update", response_class=HTMLResponse)
def actualizar_unidad_form(
    request: Request,
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "supervisor"])
):
    """
    Renderiza el formulario para actualizar una unidad de transporte.
    """
    return templates.TemplateResponse("ActualizarTransport.html", {"request": request})

@app.get("/delete", response_class=HTMLResponse)
def eliminar_unidad_form(
    request: Request,
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "supervisor"])
):
    """
    Renderiza el formulario para eliminar una unidad de transporte.
    """
    return templates.TemplateResponse("EliminarTransport.html", {"request": request})

@app.post("/create")
def crear_unidad(
    Ubicacion: str = Form(...),
    Capacidad: int = Form(...),
    IDRuta: int = Form(...),
    IDTipo: int = Form(...),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "supervisor"])
):
    """
    Crea una unidad de transporte con los datos proporcionados.
    """
    transport = Transport(Ubicacion=Ubicacion, Capacidad=Capacidad, IDRuta=IDRuta, IDTipo=IDTipo)
    try:
        controller.add(transport)
        return {"message": "Unidad de transporte creada exitosamente.", "data": transport.to_dict()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/update")
def actualizar_unidad(
    ID: int = Form(...),
    Ubicacion: str = Form(...),
    Capacidad: int = Form(...),
    IDRuta: int = Form(...),
    IDTipo: int = Form(...),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "supervisor"])
):
    """
    Actualiza la información de una unidad de transporte existente.
    """
    existing_transport = controller.get_by_id(Transport, ID)
    if not existing_transport:
        raise HTTPException(status_code=404, detail="Unidad de transporte no encontrada")

    updated_transport = Transport(ID=ID, Ubicacion=Ubicacion, Capacidad=Capacidad, IDRuta=IDRuta, IDTipo=IDTipo)
    try:
        controller.update(updated_transport)
        return {"message": "Unidad de transporte actualizada exitosamente.", "data": updated_transport.to_dict()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/delete")
def eliminar_unidad(
    ID: int = Form(...),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "supervisor"])
):
    """
    Elimina una unidad de transporte existente por su ID.
    """
    existing_transport = controller.get_by_id(Transport, ID)
    if not existing_transport:
        raise HTTPException(status_code=404, detail="Unidad de transporte no encontrada")

    try:
        controller.delete(existing_transport)
        return {"message": "Unidad de transporte eliminada exitosamente."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
