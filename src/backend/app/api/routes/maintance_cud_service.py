from fastapi import APIRouter, Form, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from backend.app.models.maintainance import MaintenanceCreate, MaintenanceOut
from backend.app.logic.universal_controller_sql import UniversalController
from datetime import datetime

app = APIRouter(prefix="/maintainance", tags=["maintainance"]) 
controller = UniversalController() 
templates = Jinja2Templates(directory="src/backend/app/templates")

# Route to create a maintenance record
@app.get("/crear", response_class=HTMLResponse)
def crear_mantenimiento(request: Request):
    """
    Define the GET route to display the maintenance creation form.
    """
    return templates.TemplateResponse("CrearMantenimiento.html", {"request": request})

# Route to delete a maintenance record
@app.get("/eliminar", response_class=HTMLResponse)
def eliminar_mantenimiento(request: Request):
    """
    Define the GET route to display the maintenance deletion form.
    """
    return templates.TemplateResponse("EliminarMantenimiento.html", {"request": request})

# Route to update a maintenance record
@app.get("/actualizar", response_class=HTMLResponse)
def actualizar_mantenimiento(request: Request):
    """
    Define the GET route to display the maintenance update form.
    """
    return templates.TemplateResponse("ActualizarMantenimiento.html", {"request": request})

# Route to add a new maintenance record
@app.post("/create")
async def add(
    id_unit: int = Form(...),
    id_status: int = Form(...),
    type: str = Form(...),
    date: datetime = Form(...),
):
    """
    Define the POST route to add a new maintenance record.
    It receives maintenance information and creates a MaintenanceCreate object.
    """
    mantainment_temp = MaintenanceCreate(
        id_unit=id_unit, id_status=id_status, type=type, date=date
    )
    try:
        # Attempt to add the maintenance record using the controller
        controller.add(mantainment_temp)
        return {"message": "Maintenance added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))  # Handle any exceptions.

# Route to update an existing maintenance record
@app.post("/update")
async def update(
    id: int = Form(...),
    id_unit: int = Form(...),
    id_status: int = Form(...),
    type: str = Form(...),
    date: datetime = Form(...),
):
    """
    Define the POST route to update an existing maintenance record.
    It checks if the maintenance record exists, and if so, updates it with the new data.
    """
    existing_mantainment = controller.get_by_id(MaintenanceOut, id)
    if not existing_mantainment:
        raise HTTPException(status_code=404, detail="Maintenance not found")
    
    mantainment_temp = MaintenanceCreate(
        id=id,  # The ID must remain the same to update the object
        id_unit=id_unit,
        id_status=id_status,
        type=type,
        date=date
    )
    
    try:
        # Attempt to update the maintenance record using the controller
        controller.update(mantainment_temp)
        return {"message": f"Maintenance {id} updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))  # Handle any exceptions.

# Route to delete an existing maintenance record
@app.post("/delete")
async def delete_mantainment(id: int = Form(...)):
    """
    Define the POST route to delete an existing maintenance record.
    It searches for the maintenance by ID, and if it exists, deletes it.
    """
    try:
        existing_mantainment = controller.get_by_id(MaintenanceOut, id)
        if not existing_mantainment:
            raise HTTPException(status_code=404, detail="Maintenance not found")
        
        # Delete the maintenance record using the controller
        controller.delete(existing_mantainment)
        return {"message": f"Maintenance {id} deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))  # Handle any exceptions.
