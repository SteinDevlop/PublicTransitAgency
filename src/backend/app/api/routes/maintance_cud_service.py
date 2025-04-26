from fastapi import APIRouter, Form, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from backend.app.models.maintainance import MaintenanceCreate, MaintenanceOut
from backend.app.logic.universal_controller_sql import UniversalController
from datetime import datetime

# Inicializa el router y controlador
app = APIRouter(prefix="/maintainance", tags=["maintainance"])
controller = UniversalController()
templates = Jinja2Templates(directory="src/backend/app/templates")


# Ruta para crear un mantenimiento
@app.get("/crear", response_class=HTMLResponse)
def crear_mantenimiento(request: Request):
    return templates.TemplateResponse("CrearMantenimiento.html", {"request": request})

# Ruta para eliminar un mantenimiento
@app.get("/eliminar", response_class=HTMLResponse)
def eliminar_mantenimiento(request: Request):
    return templates.TemplateResponse("EliminarMantenimiento.html", {"request": request})

# Ruta para actualizar un mantenimiento
@app.get("/actualizar", response_class=HTMLResponse)
def actualizar_mantenimiento(request: Request):
    return templates.TemplateResponse("ActualizarMantenimiento.html", {"request": request})

# Ruta para agregar un mantenimiento
@app.post("/create")
async def add(
    id_unit: int = Form(...),
    id_status: int = Form(...),
    type: str = Form(...),
    date: datetime = Form(...),
):
    # Crear una instancia de MaintenanceCreate
    mantainment_temp = MaintenanceCreate(
        id_unit=id_unit, id_status=id_status, type=type, date=date
    )
    try:
        # Agregar mantenimiento utilizando el controlador
        controller.add(mantainment_temp)
        return {"message": "Mantenimiento agregado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Ruta para actualizar un mantenimiento
@app.post("/update")
async def update(
    id: int = Form(...),
    id_unit: int = Form(...),
    id_status: int = Form(...),
    type: str = Form(...),
    date: datetime = Form(...),
):
    # Buscar el mantenimiento existente
    existing_mantainment = controller.get_by_id(MaintenanceOut, id)
    if not existing_mantainment:
        raise HTTPException(status_code=404, detail="Mantenimiento no encontrado")
    
    # Crear una instancia de MaintenanceCreate con el nuevo tipo y fecha
    mantainment_temp = MaintenanceCreate(
        id=id,  # El ID debe ser el mismo para actualizar el objeto
        id_unit=id_unit,
        id_status=id_status,
        type=type,
        date=date
    )
    
    try:
        # Actualizar el mantenimiento
        controller.update(mantainment_temp)
        return {"message": f"Mantenimiento {id} actualizado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Ruta para eliminar un mantenimiento
@app.post("/delete")
async def delete_mantainment(id: int = Form(...)):
    try:
        # Buscar el mantenimiento existente
        existing_mantainment = controller.get_by_id(MaintenanceOut, id)
        if not existing_mantainment:
            raise HTTPException(status_code=404, detail="Mantenimiento no encontrado")
        
        # Eliminar el mantenimiento
        controller.delete(existing_mantainment)
        return {"message": f"Mantenimiento {id} eliminado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
