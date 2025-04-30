from fastapi import FastAPI, HTTPException, APIRouter, Depends, Request
from typing import List
from backend.app.models.transport import TransportOut
from backend.app.logic.universal_controller_sql import UniversalController
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
import uvicorn

app = APIRouter(prefix="/transports", tags=["Transports"])
controller = UniversalController()
templates = Jinja2Templates(directory="src/backend/app/templates")

# Helper function to determine response type
def _respond(data, request: Request, template: str = None):
    accept_header = request.headers.get("Accept", "")
    if "text/html" in accept_header and template:
        return templates.TemplateResponse(template, {"request": request, "transports": data if isinstance(data, list) else [data]})
    return JSONResponse(content={"data": [item.dict() for item in data] if isinstance(data, list) else data.dict()})

@app.get("/", response_class=HTMLResponse)
async def get_all_transports(request: Request):
    """Obtiene todos los registros de transporte (HTML o JSON)."""
    try:
        transports = controller.get_all(TransportOut)
        return _respond(transports, request, "ListarTransports.html")
    except Exception as e:
        raise HTTPException(500, detail=f"Error interno del servidor: {str(e)}")

@app.get("/{transport_id}", response_class=HTMLResponse)
async def get_transport_by_id(request: Request, transport_id: str):
    """Obtiene un registro de transporte por su ID (HTML o JSON)."""
    transport = controller.get_by_id(TransportOut, transport_id)
    if transport:
        return _respond(transport, request, "DetalleTransport.html")
    else:
        raise HTTPException(404, detail=f"Transporte con ID {transport_id} no encontrado")

if __name__ == "__main__":
    app_main = FastAPI()
    app_main.include_router(app)
    uvicorn.run(app_main, host="0.0.0.0", port=8004, reload=True)