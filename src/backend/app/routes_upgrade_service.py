
from fastapi import APIRouter, Query
from logic.routes import Routes
from logic import universal_controller_json

router = APIRouter()
routes_controller = universal_controller_json()


@router.put("/routes/{route_id}")
def update_route(route_id: str, updated_data: dict):
    ruta_existente = routes_controller.get_by_id("routes", route_id)
    if not ruta_existente:
        return {"error": "Ruta no encontrada"}

    ruta_existente.route = updated_data
    ruta_existente.route_id = updated_data.get("route_id", route_id)
    routes_controller.update("routes", route_id, ruta_existente)
    return {"message": "Ruta actualizada exitosamente"}
