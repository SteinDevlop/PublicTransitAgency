from fastapi import APIRouter, Form, HTTPException, Security
from backend.app.models.stops import Parada
from backend.app.logic.universal_controller_sqlserver import UniversalController
from starlette.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
from backend.app.core.auth import get_current_user

app = APIRouter(prefix="/stops", tags=["stops"])
controller = UniversalController()
templates = Jinja2Templates(directory="src/backend/app/templates")

@app.get("/create", response_class=HTMLResponse)
def crear_parada_form(
    request: Request,
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    """
    Renderiza el formulario para crear una nueva parada.
    """
    return templates.TemplateResponse("CrearParada.html", {"request": request})

@app.get("/update", response_class=HTMLResponse)
def actualizar_parada_form(
    request: Request,
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    """
    Renderiza el formulario para actualizar una parada existente.
    """
    return templates.TemplateResponse("ActualizarParada.html", {"request": request})

@app.get("/delete", response_class=HTMLResponse)
def eliminar_parada_form(
    request: Request,
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    """
    Renderiza el formulario para eliminar una parada.
    """
    return templates.TemplateResponse("EliminarParada.html", {"request": request})

@app.post("/create")
def crear_parada(
    ID: int = Form(...),
    Nombre: str = Form(...),
    Ubicacion: str = Form(...),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    """
    Crea una nueva parada.
    """
    parada = Parada(ID=ID, Nombre=Nombre, Ubicacion=Ubicacion)
    try:
        controller.add(parada)
        return {"message": "Parada creada exitosamente.", "data": parada.to_dict()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al crear la parada: {str(e)}")

@app.post("/update")
def actualizar_parada(
    ID: int = Form(...),
    Nombre: str = Form(...),
    Ubicacion: str = Form(...),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    """
    Actualiza una parada existente.
    """
    existing_parada = controller.get_by_id(Parada, ID)
    if not existing_parada:
        raise HTTPException(status_code=404, detail="Parada no encontrada")

    parada_actualizada = Parada(ID=ID, Nombre=Nombre, Ubicacion=Ubicacion)
    try:
        controller.update(parada_actualizada)
        return {"message": "Parada actualizada exitosamente.", "data": parada_actualizada.to_dict()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al actualizar la parada: {str(e)}")

@app.post("/delete")
def eliminar_parada(
    ID: int = Form(...),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    """
    Elimina una parada por su ID.
    """
    existing_parada = controller.get_by_id(Parada, ID)
    if not existing_parada:
        raise HTTPException(status_code=404, detail="Parada no encontrada")

    try:
        controller.delete(existing_parada)
        return {"message": "Parada eliminada exitosamente."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al eliminar la parada: {str(e)})
