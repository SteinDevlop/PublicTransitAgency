from fastapi import APIRouter, HTTPException
from logic.incidence import Incidence
from logic.universal_controller_json import UniversalController

router = APIRouter()
controller = UniversalController()

@router.post("/incidence/create")
def create_incidence(description: str, type: str, status: str, incidence_id: int):
    try:
        incidence = Incidence(description, type, status, incidence_id)
        controller.add(incidence)
        return {"message": "Incidencia registrada exitosamente."}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))