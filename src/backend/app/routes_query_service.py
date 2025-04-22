from fastapi import FastAPI
from logic.routes import Routes
from logic.universal_controller_json import UniversalController

app = FastAPI()
controller = UniversalController()

@app.get("/routes")
def list_all_routes():
    all_routes = controller.get_all("routes")
    return {"routes": [r.__dict__ for r in all_routes]}

@app.get("/routes/{route_id}")
def get_route_by_id(route_id: str):
    route = controller.get_by_id("routes", route_id)
    if not route:
        return {"error": "Ruta no encontrada"}
    return {"route": route.__dict__}
