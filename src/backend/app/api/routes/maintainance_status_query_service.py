from fastapi import FastAPI, HTTPException, Request, Query, APIRouter
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from backend.app.models.maintainance_status import MaintainanceStatusOut  # Modelo
from backend.app.logic.universal_controller_sql import UniversalController
import uvicorn

# Initialize the FastAPI router for the "maintainance_status" functionality
app = APIRouter(prefix="/maintainance_status", tags=["mantenimiento"])

# Initialize the controller
controller = UniversalController()

templates = Jinja2Templates(directory="src/backend/app/templates")

# Route to consult and display the list of maintainance statuses
@app.get('/consultar', response_class=HTMLResponse)
def consultar_mantenimientos(request: Request):
    """
    Renderiza el template 'consultar_mantenimientos.html' para mostrar la lista.
    """
    return templates.TemplateResponse("consultar_mantenimientos.html", {"request": request})

# Route to get all maintainance statuses (returns JSON)
@app.get("/all")
async def get_all_statuses():
    """
    Retorna todos los registros de estados de mantenimiento en formato JSON.
    """
    records = controller.read_all(MaintainanceStatusOut)
    return JSONResponse(content={"data": records})

# Route to view a specific maintainance status by its ID (renders HTML)
@app.get("/get", response_class=HTMLResponse)
async def get_status_by_id_html(request: Request, id: int = Query(...)):
    """
    Obtiene un estado de mantenimiento por su ID y renderiza los detalles en HTML.
    """
    unit_status = controller.get_by_id(MaintainanceStatusOut, id)

    if unit_status:
        return templates.TemplateResponse("detalle_mantenimiento.html", {"request": request, "data": unit_status})
    else:
        raise HTTPException(status_code=404, detail="Estado de mantenimiento no encontrado")

# Route to get a specific maintainance status by its ID (returns JSON)
@app.get("/get/json")
async def get_status_by_id_json(id: int = Query(...)):
    """
    Obtiene un estado de mantenimiento por su ID en formato JSON.
    """
    unit_status = controller.get_by_id(MaintainanceStatusOut, id)
    if unit_status:
        return JSONResponse(content={"data": unit_status.dict()})
    else:
        raise HTTPException(status_code=404, detail="Estado de mantenimiento no encontrado")

if __name__ == "__main__":
    app_main = FastAPI()
    app_main.include_router(app)
    uvicorn.run(app_main, host="0.0.0.0", port=8003)