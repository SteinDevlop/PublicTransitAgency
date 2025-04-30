from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from backend.app.models.routes import RouteOut
from backend.app.logic.universal_controller_sql import UniversalController
import uvicorn

app = FastAPI()
controller = UniversalController()
templates = Jinja2Templates(directory="src/backend/app/templates")

# Configuración CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Endpoints GET para formularios HTML
@app.get("/routes", response_class=HTMLResponse, tags=["routes"])
def show_all_routes(request: Request):
    routes = controller.read_all(RouteOut(route_id=0, route=""))
    return templates.TemplateResponse("ConsultarRutas.html", {"request": request, "routes": routes})

@app.get("/routes/{route_id}", response_class=HTMLResponse, tags=["routes"])
def show_route(request: Request, route_id: int):
    route = controller.get_by_id(RouteOut, route_id)
    if not route:
        raise HTTPException(status_code=404, detail="Ruta no encontrada")
    return templates.TemplateResponse("ConsultarRutaDetalle.html", {"request": request, "route": route})

# Endpoints POST para operaciones
@app.post("/routes/search", response_model=RouteOut, tags=["routes"])
async def search_route(
    request: Request,
    route_id: int = Form(...),
):
    try:
        route = controller.get_by_id(RouteOut, route_id)
        if not route:
            raise HTTPException(status_code=404, detail="Ruta no encontrada")
        return route
    except ValueError as e:
        raise HTTPException(400, detail=str(e))
    except Exception as e:
        raise HTTPException(500, detail=f"Error interno del servidor: {str(e)}")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)
