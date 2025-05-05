from fastapi import APIRouter, Form, HTTPException, Security
from backend.app.logic.universal_controller_postgres import UniversalController
from backend.app.models.stops import Stop
from backend.app.core.auth import get_current_user

app = APIRouter(prefix="/stops", tags=["stops"])
controller = UniversalController()

@app.post("/create")
def crear_parada(
    id: int = Form(...),
    nombre: str = Form(...),
    ubicacion: str = Form(...),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "supervisor"])
):
    parada = Stop(id=id, nombre=nombre, ubicacion=ubicacion)
    try:
        controller.add(parada)
        return {"message": "Parada creada exitosamente."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/update")
def actualizar_parada(
    id: int = Form(...),
    nombre: str = Form(...),
    ubicacion: str = Form(...),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "supervisor"])
):
    parada = Stop(id=id, nombre=nombre, ubicacion=ubicacion)
    try:
        controller.update(parada)
        return {"message": "Parada actualizada exitosamente."}
    except Exception as e:
        raise HTTPException(status_code=404, detail="Parada no encontrada")

@app.post("/delete")
def eliminar_parada(
    id: int = Form(...),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "supervisor"])
):
    parada = Stop(id=id, nombre="", ubicacion="")
    try:
        controller.delete(parada)
        return {"message": "Parada eliminada exitosamente."}
    except Exception as e:
        raise HTTPException(status_code=404, detail="Parada no encontrada")