from fastapi import FastAPI, HTTPException
from logic.mantainment import Maintenance
from logic.mantainment_controller import Controller

app = FastAPI()
controller_maintenance = Controller()

@app.get("/maintenance")
def get_all():
    """
    Retorna todos los datos de mantenimiento.
    """
    return controller_maintenance.get_all()

@app.get("/maintenance/{id}")
def get_by_id(id: int):
    """
    Retorna el dato de un mantenimiento por su ID.
    """
    result = controller_maintenance.get_by_id(id)
    if not result:
        raise HTTPException(status_code=404, detail="No encontrado")
    return result.to_dict()

@app.get("/maintenance/unit/{unit_id}")
def get_by_unit(unit_id: int):
    """
    Retorna todos los mantenimientos asociados a una unidad.
    """
    return controller_maintenance.get_by_unit(unit_id)
