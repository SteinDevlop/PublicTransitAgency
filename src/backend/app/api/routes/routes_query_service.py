from fastapi import FastAPI, APIRouter, Request, Query
from fastapi.responses import HTMLResponse
from fastapi import HTTPException
from fastapi.templating import Jinja2Templates
from backend.app.models.routes import RouteOut
from backend.app.logic.universal_controller_sql import UniversalController

app = APIRouter(prefix="/routes", tags=["routes"])
controller = UniversalController()
templates = Jinja2Templates(directory="src/backend/app/templates")

@app.get("/listar", response_class=HTMLResponse)
def list_routes_page(request: Request):
    routes = controller.read_all(RouteOut)
    return templates.TemplateResponse("ListarRutas.html", {"request": request, "routes": routes}) 

@app.get("/detalles/{route_id}", response_class=HTMLResponse)
def route_detail_page(request: Request, route_id: str):
    route = controller.get_by_id(RouteOut, route_id)
    return templates.TemplateResponse("DetalleRuta.html", {"request": request, "route": route}) 

@app.get("/all")
async def get_all_routes():
    return controller.read_all(RouteOut)

@app.get("/{route_id}")
async def get_route_by_id(route_id: str):
    route = controller.get_by_id(RouteOut, route_id)
    if route:
        return route
    raise HTTPException(404, detail="Route not found")