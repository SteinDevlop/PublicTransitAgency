from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models.routes import RouteOut
from logic.universal_controller_sql import UniversalController
import uvicorn

app = FastAPI()
controller = UniversalController()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

@app.get("/routes")
async def list_all_routes():
    dummy = RouteOut.get_empty_instance()
    routes = controller.read_all(dummy)
    return {"data": routes}

@app.get("/routes/{route_id}")
async def get_route(route_id: str):
    route = controller.get_by_id(RouteOut, route_id)
    if not route:
        raise HTTPException(404, detail="Ruta no encontrada")
    return {"data": route}

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8002, reload=True)