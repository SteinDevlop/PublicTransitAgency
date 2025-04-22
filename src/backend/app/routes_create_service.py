from fastapi import FastAPI, Request
from logic.routes import Routes
from logic.universal_controller_json import UniversalController

app = FastAPI()
controller = UniversalController()

@app.post("/routes")
async def create_route(request: Request):
    data = await request.json()

    route = data.get("route")
    route_id = data.get("route_id")

    if not route or not route_id:
        return {"error": "Both 'route' and 'route_id' are required in the request body."}

    try:
        new_route = Routes(route, route_id)
        controller.save(new_route)
        return {"message": "Route created successfully"}
    except Exception as e:
        return {"error": str(e)}
