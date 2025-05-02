from fastapi import FastAPI, HTTPException, Request, Query, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from backend.app.models.stops import StopOut
from backend.app.logic.universal_controller_sql import UniversalController
import uvicorn

# Initialize the FastAPI router for the "stops" functionality
app = APIRouter(prefix="/stops", tags=["stops"])

controller = UniversalController()
templates = Jinja2Templates(directory="src/backend/app/templates")

@app.get("/", response_class=HTMLResponse)
def listar_paradas(request):
    """Lista todas las paradas en formato HTML."""
    paradas = controller.read_all(StopOut(stop_id=0, stop_data={}))
    return templates.TemplateResponse("ListarParadas.html", {"request": request, "paradas": paradas})

@app.get("/{stop_id}", response_class=HTMLResponse)
def detalle_parada(stop_id: int, request):
    """Obtiene una parada por su ID y la muestra en HTML."""
    parada = controller.get_by_id(StopOut, stop_id)
    if not parada:
        raise HTTPException(status_code=404, detail="Parada no encontrada")
    return templates.TemplateResponse("DetalleParada.html", {"request": request, "parada": parada})


if __name__ == "__main__":
    app_main = FastAPI()
    app_main.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["GET"],
        allow_headers=["*"],
    )
    app_main.include_router(app)
    uvicorn.run(app_main, host="0.0.0.0", port=8008)