from fastapi import FastAPI, HTTPException, Request, Query
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from backend.app.models.incidence import IncidenceOut
from logic.universal_controller_sql import UniversalController
import uvicorn

app = FastAPI(
    title="Query Service - Incidencias",
    description="Microservicio para consulta de incidencias",
    version="1.0.0"
)

controller = UniversalController()
templates = Jinja2Templates(directory="src/backend/app/templates")

# Configuración CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

@app.get("/incidence/consultar", response_class=HTMLResponse)
async def consultar_incidencias(request: Request):
    """
    Página con opciones para consultar incidencias
    """
    return templates.TemplateResponse("ConsultarIncidencias.html", {"request": request})

@app.get("/incidence/todos", response_class=HTMLResponse)
async def get_all_incidences(request: Request):
    """
    Obtiene todas las incidencias registradas
    """
    dummy = IncidenceOut.get_empty_instance()
    data = controller.read_all(dummy)

    if "text/html" in request.headers.get("accept", ""):
        return templates.TemplateResponse(
            "ListaIncidencias.html",
            {"request": request, "incidencias": data}
        )
    
    return {"data": data}

@app.get("/incidence/detalle", response_class=HTMLResponse)
async def get_incidence_by_id(
    request: Request,
    id: int = Query(..., description="ID de la incidencia")
):
    """
    Consulta una incidencia específica por su ID
    """
    incidence = controller.get_by_id(IncidenceOut, id)
    if not incidence:
        if "text/html" in request.headers.get("accept", ""):
            return templates.TemplateResponse(
                "DetalleIncidencia.html",
                {"request": request, "error": "Incidencia no encontrada"},
                status_code=404
            )
        raise HTTPException(404, detail="Incidencia no encontrada")

    if "text/html" in request.headers.get("accept", ""):
        return templates.TemplateResponse(
            "DetalleIncidencia.html",
            {"request": request, "estado": incidence}
        )
    
    return {"data": incidence}

if __name__ == "__main__":
    uvicorn.run("incidence_query_service:app", host="0.0.0.0", port=8003, reload=True)
