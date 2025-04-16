from fastapi import APIRouter, Query
from logic.routes import Routes
from logic import universal_controller_json

router = APIRouter()
routes_controller = universal_controller_json()

@router.get("/routes")
def list_all_routes():
    all_routes = routes_controller.get_all("routes")
    return {"routes": [r.__dict__ for r in all_routes]}

@router.get("/routes/by-id")
def get_route_by_id(route_id: str = Query(...)):
    route = routes_controller.get_by_id("routes", route_id)
    if not route:
        return {"error": "Ruta no encontrada"}
    return {"route": route.__dict__}


