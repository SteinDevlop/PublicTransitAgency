from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models.routes import RouteCreate, RouteOut
from logic.universal_controller_sql import UniversalController
import uvicorn

app = FastAPI()
controller = UniversalController()

# CORS (always included)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"],
)

@app.post("/routes/create")
async def create_route(request: Request):
    try:
        data = await request.json()
        route_data = data.get("route")
        route_id = data.get("route_id")
        
        if not route_data or not route_id:
            raise ValueError("Both 'route' and 'route_id' are required")
        
        route = RouteCreate(route=route_data, route_id=route_id)
        result = controller.add(route.to_dict())
        
        return {
            "operation": "create",
            "success": True,
            "data": result,
            "message": "Ruta creada exitosamente"
        }
    except ValueError as e:
        raise HTTPException(400, detail=str(e))
    except Exception as e:
        raise HTTPException(500, detail="Error interno del servidor")

@app.post("/routes/update")
async def update_route(request: Request):
    try:
        data = await request.json()
        route_data = data.get("route")
        route_id = data.get("route_id")
        
        existing = controller.get_by_id(RouteOut, route_id)
        if not existing:
            raise HTTPException(404, detail="Ruta no encontrada")
        
        updated_route = RouteCreate(route=route_data, route_id=route_id)
        result = controller.update(updated_route.to_dict())
        
        return {
            "operation": "update",
            "success": True,
            "data": result,
            "message": f"Ruta {route_id} actualizada"
        }
    except ValueError as e:
        raise HTTPException(400, detail=str(e))

@app.post("/routes/delete")
async def delete_route(request: Request):
    try:
        data = await request.json()
        route_id = data.get("route_id")
        
        existing = controller.get_by_id(RouteOut, route_id)
        if not existing:
            raise HTTPException(404, detail="Ruta no encontrada")
        
        controller.delete(existing)
        return {
            "operation": "delete",
            "success": True,
            "message": f"Ruta {route_id} eliminada"
        }
    except Exception as e:
        raise HTTPException(500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8001, reload=True)
