from fastapi import FastAPI, HTTPException, Request, Query, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from backend.app.models.stops import StopOut
from logic.universal_controller_sql import UniversalController
import uvicorn

# Initialize the FastAPI router for the "stops" functionality
app = APIRouter(prefix="/stops", tags=["paradas"])

controller = UniversalController()
templates = Jinja2Templates(directory="templates")  # Asegúrate de tener las plantillas en este directorio

# Endpoint para la página de consulta principal (HTML)
@app.get("/consultar", response_class=HTMLResponse)
async def consultar_paradas_html(request: Request):
    """Renderiza la página para consultar paradas."""
    return templates.TemplateResponse("consultar_paradas.html", {"request": request})

# Endpoint para obtener todas las paradas (HTML)
@app.get("", response_class=HTMLResponse)
async def listar_paradas_html(request: Request):
    """Lista todas las paradas en formato HTML."""
    dummy = StopOut.get_empty_instance()
    paradas = controller.read_all(dummy)
    return templates.TemplateResponse("listar_paradas.html", {"request": request, "paradas": paradas})

# Endpoint para obtener todas las paradas (JSON)
@app.get("/json")
async def listar_paradas_json():
    """Lista todas las paradas en formato JSON."""
    dummy = StopOut.get_empty_instance()
    paradas = controller.read_all(dummy)
    return JSONResponse(content={"data": [parada.dict() for parada in paradas]})

# Endpoint para obtener una parada por ID (HTML)
@app.get("/{stop_id}", response_class=HTMLResponse)
async def obtener_parada_html(request: Request, stop_id: str):
    """Obtiene una parada por su ID y la muestra en HTML."""
    parada = controller.get_by_id(StopOut, stop_id)
    if not parada:
        raise HTTPException(status_code=404, detail="Parada no encontrada")
    return templates.TemplateResponse("detalle_parada.html", {"request": request, "parada": parada})

# Endpoint para obtener una parada por ID (JSON)
@app.get("/{stop_id}/json")
async def obtener_parada_json(stop_id: str):
    """Obtiene una parada por su ID en formato JSON."""
    parada = controller.get_by_id(StopOut, stop_id)
    if not parada:
        raise HTTPException(status_code=404, detail="Parada no encontrada")
    return JSONResponse(content={"data": parada.dict()})

# Endpoint para buscar paradas (HTML)
@app.get("/buscar", response_class=HTMLResponse)
async def buscar_paradas_html(request: Request, nombre: str = Query(None), ubicacion: str = Query(None)):
    """Busca paradas por nombre y/o ubicación y muestra los resultados en HTML."""
    dummy = StopOut.get_empty_instance()
    todas_las_paradas = controller.read_all(dummy)
    filtradas = []
    for parada in todas_las_paradas:
        parada_data = parada.stop_data
        coincide = True
        if nombre and nombre.lower() not in parada_data.get('name', '').lower():
            coincide = False
        if ubicacion and ubicacion.lower() not in parada_data.get('location', '').lower():
            coincide = False
        if coincide:
            filtradas.append(parada)

    if filtradas:
        return templates.TemplateResponse("resultados_busqueda.html", {"request": request, "paradas": filtradas})
    else:
        return templates.TemplateResponse("sin_resultados.html", {"request": request})

# Endpoint para buscar paradas (JSON)
@app.get("/buscar/json")
async def buscar_paradas_json(nombre: str = Query(None), ubicacion: str = Query(None)):
    """Busca paradas por nombre y/o ubicación y devuelve los resultados en JSON."""
    dummy = StopOut.get_empty_instance()
    todas_las_paradas = controller.read_all(dummy)
    filtradas = []
    for parada in todas_las_paradas:
        parada_data = parada.stop_data
        coincide = True
        if nombre and nombre.lower() not in parada_data.get('name', '').lower():
            coincide = False
        if ubicacion and ubicacion.lower() not in parada_data.get('location', '').lower():
            coincide = False
        if coincide:
            filtradas.append(parada.dict())

    return JSONResponse(content={"data": filtradas})

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