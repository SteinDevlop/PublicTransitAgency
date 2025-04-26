from fastapi import FastAPI, HTTPException, APIRouter, Form, Request
from backend.app.logic.mantainment_controller import Controller

controller_maintenance = Controller()
app = APIRouter(prefix="/maintainance", tags=["maintainance"])

@app.get("/maintainancements", response_model=list[dict])
def get_all():
    """
    Returns all maintenance data.
    """
    return controller_maintenance.get_all()

@app.get("/{id}")
def get_by_id(id: int):
    """
    Returns a maintenance record by its ID.
    If not found, raises a 404 error.
    """
    result = controller_maintenance.get_by_id(id)
    if not result:
        raise HTTPException(status_code=404, detail="Not found")
    return result.to_dict()

@app.get("/unit/{unit_id}")
def get_by_unit(unit_id: int):
    """
    Returns all maintenance records associated with a specific unit.
    """
    return controller_maintenance.get_by_unit(unit_id)
