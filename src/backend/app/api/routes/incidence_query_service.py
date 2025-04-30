from fastapi import FastAPI, HTTPException, Request, Query, APIRouter
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from backend.app.models.incidence import IncidenceOut  # Mismo modelo que en CUD
from logic.universal_controller_sql import UniversalController
import uvicorn

# Initialize the FastAPI router for the "incidence" functionality
app = APIRouter(prefix="/incidences", tags=["incidencias"])

controller = UniversalController()
templates = Jinja2Templates(directory="src/backend/app/templates")

# Endpoint 1: Obtener todas las incidencias (con paginación y filtro) - HTML
@app.get("", response_class=HTMLResponse)
async def listar_incidencias_html(
    request: Request,
    skip: int = Query(0, description="Registros a saltar"),
    limit: int = Query(10, description="Límite de resultados"),
    status: str = Query(None, description="Filtrar por estado (opcional)")
):
    try:
        dummy = IncidenceOut.get_empty_instance()
        all_data = controller.read_all(dummy)

        # Filtrado por estado (si se especifica)
        if status:
            filtered_data = [item for item in all_data if item.status == status]
        else:
            filtered_data = all_data

        # Paginación
        paginated_data = filtered_data[skip:skip + limit]
        return templates.TemplateResponse("ListarIncidencia.html", {"request": request, "incidencias": paginated_data})
    except Exception as e:
        raise HTTPException(500, detail=str(e))

# Endpoint 1 (JSON): Obtener todas las incidencias (con paginación y filtro) - JSON
@app.get("/json")
async def listar_incidencias_json(
    skip: int = Query(0, description="Registros a saltar"),
    limit: int = Query(10, description="Límite de resultados"),
    status: str = Query(None, description="Filtrar por estado (opcional)")
):
    try:
        dummy = IncidenceOut.get_empty_instance()
        all_data = controller.read_all(dummy)

        # Filtrado por estado (si se especifica)
        if status:
            filtered_data = [item for item in all_data if item.status == status]
        else:
            filtered_data = all_data

        # Paginación
        paginated_data = filtered_data[skip:skip + limit]
        return JSONResponse(content={"data": paginated_data})
    except Exception as e:
        raise HTTPException(500, detail=str(e))

# Endpoint 2: Obtener incidencia por ID - HTML
@app.get("/{incidence_id}", response_class=HTMLResponse)
async def obtener_incidencia_html(request: Request, incidence_id: int = Query(...)):
    try:
        incidence = controller.get_by_id(IncidenceOut, incidence_id)
        if not incidence:
            raise HTTPException(status_code=404, detail="Incidencia no encontrada")
        return templates.TemplateResponse("DetalleIncidencia.html", {"request": request, "incidencia": incidence})
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, detail=str(e))

# Endpoint 2 (JSON): Obtener incidencia por ID - JSON
@app.get("/{incidence_id}/json")
async def obtener_incidencia_json(incidence_id: int = Query(...)):
    try:
        incidence = controller.get_by_id(IncidenceOut, incidence_id)
        if not incidence:
            raise HTTPException(status_code=404, detail="Incidencia no encontrada")
        return JSONResponse(content={"data": incidence.dict()})
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, detail=str(e))

# Endpoint para la página de consulta principal (HTML)
@app.get("/consultar", response_class=HTMLResponse)
def consultar_incidencias(request: Request):
    return templates.TemplateResponse("ConsultarIncidencia", {"request": request})

if __name__ == "__main__":
    app_main = FastAPI(
        title="Query Service - Incidencias",
        description="Microservicio para consulta de incidencias",
        version="1.0.0"
    )
    app_main.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["GET"],
        allow_headers=["*"],
    )
    app_main.include_router(app)
    uvicorn.run(app_main, host="0.0.0.0", port=8002, reload=True)