from fastapi import FastAPI, HTTPException, Request, Query  # <-- Añade Query aquí
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from backend.app.models.maintainance_status import MaintainanceStatusOut
from backend.app.logic.universal_controller_sql import UniversalController
import uvicorn

app = FastAPI(
    title="Query Service - Estados de Mantenimiento",
    description="Microservicio para consulta de estados de mantenimiento",
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

@app.get("/maintainance_status/consultar", response_class=HTMLResponse)
async def consultar_estados(request: Request):
    """
    Endpoint principal para consultar estados de mantenimiento
    """
    return templates.TemplateResponse("ConsultarEstados.html", {"request": request})

@app.get("/maintainance_status/todos", response_class=HTMLResponse)
async def get_all_maintainance_status(request: Request):
    """
    Obtiene todos los estados de mantenimiento
    """
    dummy = MaintainanceStatusOut.get_empty_instance()
    data = controller.read_all(dummy)

    if "text/html" in request.headers.get("Accept", ""):
        return templates.TemplateResponse(
            "ListaEstados.html",
            {"request": request, "estados": data}
        )
    
    return {"data": data}

@app.get("/maintainance_status/detalle", response_class=HTMLResponse)
async def get_maintainance_status(
    request: Request,
    id: int = Query(..., description="ID del estado de mantenimiento")  # <-- Ahora funciona correctamente
):
    """
    Obtiene un estado de mantenimiento específico por ID
    """
    status = controller.get_by_id(MaintainanceStatusOut, id)
    if not status:
        if "text/html" in request.headers.get("Accept", ""):
            return templates.TemplateResponse(
                "DetalleEstado.html",
                {"request": request, "error": "Estado no encontrado"},
                status_code=404
            )
        raise HTTPException(404, detail="Estado de mantenimiento no encontrado")

    if "text/html" in request.headers.get("Accept", ""):
        return templates.TemplateResponse(
            "DetalleEstado.html",
            {"request": request, "estado": status}
        )
    
    return {"data": status}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8002, reload=True)