from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from backend.app.models.routes import RouteOut
from logic.universal_controller_sql import UniversalController
import uvicorn

app = FastAPI()
controller = UniversalController()

# Jinja2 Templates configuration
templates = Jinja2Templates(directory="src/backend/app/templates")

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

# Endpoint to display all routes in HTML
@app.get("/routes", response_class=HTMLResponse, tags=["routes"])
async def list_all_routes(request: Request):
    dummy = RouteOut.get_empty_instance()
    try:
        routes = controller.read_all(dummy)
        return templates.TemplateResponse(
            "ListarRutas.html", {"request": request, "routes": routes}
        )
    except Exception as e:
        raise HTTPException(500, detail="Error al obtener las rutas")

# Endpoint to display a single route by ID in HTML
@app.get("/routes/{route_id}", response_class=HTMLResponse, tags=["routes"])
async def get_route(request: Request, route_id: str):
    try:
        route = controller.get_by_id(RouteOut, route_id)
        if not route:
            raise HTTPException(404, detail="Ruta no encontrada")
        return templates.TemplateResponse(
            "DetalleRuta.html", {"request": request, "route": route}
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(500, detail="Error al obtener la ruta")

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8002, reload=True)
