from fastapi import APIRouter, Request
from logic.routes import Routes
from src.backend.app.logic.universal_controller_json import UniversalJSONController

router = APIRouter()
controller = UniversalJSONController("routes")

@router.post("/routes/create")
def create_route(request: Request, route: dict):
    if "route_id" not in route:
        return {"error": "route_id is required in route dict"}

    new_route = Routes(route, route["route_id"])
    controller.save(new_route)
    return {"message": "Route created successfully"}  
