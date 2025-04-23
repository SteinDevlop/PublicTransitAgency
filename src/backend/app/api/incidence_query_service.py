from fastapi import APIRouter, HTTPException, Query
from logic.incidence import Incidence
from logic.universal_controller_json import UniversalController

router = APIRouter()
controller = UniversalController()

@router.get("/incidence/list")
def list_incidences():
    return controller.read_all(Incidence("", "", "", 0))

@router.get("/incidence/{incidence_id}")
def get_incidence_by_id(incidence_id: int):
    incidence = controller.get_by_id(Incidence, incidence_id)
    if incidence:
        return incidence.to_dict()
    raise HTTPException(status_code=404, detail="Incidencia no encontrada")
@router.get("/incidence/unit_transport/{unit_transport_id}")

def get_incidences_by_unit_transport(unit_transport_id: int):
    incidences = controller.get_by_unit_transport(Incidence, unit_transport_id)
    if incidences:
        return [incidence.to_dict() for incidence in incidences]
    raise HTTPException(status_code=404, detail="No se encontraron incidencias para la unidad de transporte especificada")
