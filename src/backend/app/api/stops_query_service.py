from fastapi import APIRouter, Query
from logic.stops import Stops
from logic import universal_controller_json

router = APIRouter()
controller = universal_controller_json()

@router.get("/stops")
def get_stops(stop_id: str = Query(default=None)):
    if stop_id:
        result = controller.get_by_id(Stops, stop_id)
        return result.to_dict() if result else {"message": "Parada no encontrada"}
    else:
        return controller.read_all(Stops())
