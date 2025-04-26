from fastapi import FastAPI, HTTPException,APIRouter, Form, Request
from backend.app.logic.mantainment_controller import Controller

controller_maintenance = Controller()
app = APIRouter(prefix="/maintainance", tags=["maintainance"])
@app.get("/maintainancements", response_model=list[dict])
def get_all():
    """
    Retorna todos los datos de mantenimiento.
    """
    return controller_maintenance.get_all()

@app.get("/{id}")
def get_by_id(id: int):
    """
    Retorna el dato de un mantenimiento por su ID.
    """
    result = controller_maintenance.get_by_id(id)
    if not result:
        raise HTTPException(status_code=404, detail="No encontrado")
    return result.to_dict()

@app.get("/unit/{unit_id}")
def get_by_unit(unit_id: int):
    """
    Retorna todos los mantenimientos asociados a una unidad.
    """
    return controller_maintenance.get_by_unit(unit_id)
