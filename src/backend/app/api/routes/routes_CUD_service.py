from fastapi import FastAPI, Form, HTTPException, APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from backend.app.models.routes import RouteCreate, RouteOut
from backend.app.logic.universal_controller_sql import UniversalController

app = APIRouter(prefix="/routes", tags=["routes"])
controller = UniversalController()
templates = Jinja2Templates(directory="src/backend/app/templates")

@app.get("/crear", response_class=HTMLResponse)
def index_create(request: Request):
    return templates.TemplateResponse("CrearRuta.html", {"request": request}) # Asegúrate de tener este HTML

@app.get("/actualizar", response_class=HTMLResponse)
def index_update(request: Request):
    return templates.TemplateResponse("ActualizarRuta.html", {"request": request}) # Asegúrate de tener este HTML

@app.get("/eliminar", response_class=HTMLResponse)
def index_delete(request: Request):
    return templates.TemplateResponse("EliminarRuta.html", {"request": request}) # Asegúrate de tener este HTML

@app.post("/create")
async def create_route(
    route_id: str = Form(...),
    name: str = Form(None),
    origin: str = Form(None),
    destination: str = Form(None),
    # user = Depends(get_current_user) # Si tienes autenticación
):
    try:
        new_route = RouteCreate(
            route_id=route_id,
            name=name,
            origin=origin,
            destination=destination
        )
        result = controller.add(new_route)
        return {"operation": "create", "success": True, "data": RouteOut(**result.to_dict()).dict(), "message": "Route created successfully"}
    except ValueError as e:
        raise HTTPException(400, detail=str(e))
    except Exception as e:
        raise HTTPException(500, detail=f"Internal server error: {str(e)}")

@app.post("/update/{route_id}")
async def update_route(
    route_id: str,
    name: str = Form(None),
    origin: str = Form(None),
    destination: str = Form(None),
    # user = Depends(get_current_user) # Si tienes autenticación
):
    try:
        existing_route = controller.get_by_id(RouteOut, route_id)
        if not existing_route:
            raise HTTPException(404, detail="Route not found")

        update_data = RouteCreate(
            route_id=route_id, # ID is part of the path, ensure it's consistent
            name=name if name is not None else existing_route.name,
            origin=origin if origin is not None else existing_route.origin,
            destination=destination if destination is not None else existing_route.destination
        )
        result = controller.update(update_data)
        return {"operation": "update", "success": True, "data": RouteOut(**result.to_dict()).dict(), "message": f"Route {route_id} updated successfully"}
    except ValueError as e:
        raise HTTPException(400, detail=str(e))
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(500, detail=str(e))

@app.post("/delete/{route_id}")
async def delete_route(route_id: str):
    try:
        existing_route = controller.get_by_id(RouteOut, route_id)
        if not existing_route:
            raise HTTPException(404, detail="Route not found")
        controller.delete(existing_route)
        return {"operation": "delete", "success": True, "message": f"Route {route_id} deleted successfully"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(500, detail=str(e))