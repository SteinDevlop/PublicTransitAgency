from fastapi import APIRouter, HTTPException
from logic.stops import Stops
from logic import universal_controller_json

router = APIRouter()
controller = universal_controller_json()

@router.post("/stops")
def create_stop(stop_data: dict):
    try:
        if "stop_id" not in stop_data:
            raise HTTPException(status_code=400, detail="El campo 'stop_id' es obligatorio")

        new_stop = Stops(stop=stop_data, id=stop_data["stop_id"])
        controller.add(new_stop)

        return {"message": "Parada creada exitosamente"}

    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
