from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from backend.app.logic.universal_controller_sql import UniversalController
from backend.app.models.incidence import Incidence

app = APIRouter(prefix="/incidence", tags=["incidence"])
controller = UniversalController()
templates = Jinja2Templates(directory="src/backend/app/templates")

@app.get("/create", response_class=HTMLResponse)
def crear_incidencia_form(request: Request):
    return templates.TemplateResponse("CrearIncidencia.html", {"request": request})

@app.post("/create")
def crear_incidencia(
    ID: int = Form(...),
    IDTicket: int = Form(...),
    Descripcion: str = Form(...),
    Tipo: str = Form(...),
    IDUnidad: int = Form(...)
):
    incidencia = Incidence(
        ID=ID,
        IDTicket=IDTicket,
        Descripcion=Descripcion,
        Tipo=Tipo,
        IDUnidad=IDUnidad
    )
    try:
        controller.add(incidencia)
        return {
            "operation": "create",
            "success": True,
            "data": incidencia,
            "message": "Incidencia creada exitosamente."
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/update", response_class=HTMLResponse)
def actualizar_incidencia_form(request: Request):
    return templates.TemplateResponse("ActualizarIncidencia.html", {"request": request})

@app.post("/update")
def actualizar_incidencia(
    id: int = Form(...),
    description: str = Form(...),
    type: str = Form(...),
    status: str = Form(...),
    ticket_id: int = Form(...)
):
    incidencia = Incidence(
        id=id,
        description=description,
        type=type,
        status=status,
        ticket_id=ticket_id
    )
    try:
        controller.update(incidencia)
        return {
            "operation": "update",
            "success": True,
            "data": incidencia,
            "message": "Incidencia actualizada exitosamente."
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/delete", response_class=HTMLResponse)
def eliminar_incidencia_form(request: Request):
    return templates.TemplateResponse("EliminarIncidencia.html", {"request": request})

@app.post("/delete")
def eliminar_incidencia(id: int = Form(...)):
    incidencia = Incidence(id=id)
    try:
        controller.delete(incidencia)
        return {
            "operation": "delete",
            "success": True,
            "message": "Incidencia eliminada exitosamente."
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
        existing_incidence = controller.get_by_id(IncidenceOut, IncidenciaID)
        if not existing_incidence:
            raise HTTPException(404, detail="Incidence not found")

        updated_incidence = IncidenceCreate(
            IncidenciaID=IncidenciaID,
            Descripcion=Descripcion,
            Tipo=Tipo,
            TicketID=TicketID
        )
        result = controller.update(updated_incidence)
        return {
            "operation": "update",
            "success": True,
            "data": IncidenceOut(
                IncidenciaID=result.IncidenciaID,
                Descripcion=result.Descripcion,
                Tipo=result.Tipo,
                TicketID=result.TicketID
            ).dict(),
            "message": f"Incidence {IncidenciaID} updated successfully"
        }
    except ValueError as e:
        raise HTTPException(400, detail=str(e))
    except HTTPException as e:
        raise e
    

@app.post("/delete")
async def delete_incidence(IncidenciaID: int = Form(...)):
    """Deletes an existing incidence."""
    try:
        existing_incidence = controller.get_by_id(IncidenceOut, IncidenciaID)
        if not existing_incidence:
            raise HTTPException(404, detail="Incidence not found")
        controller.delete(existing_incidence)
        return {
            "operation": "delete",
            "success": True,
            "message": f"Incidence {IncidenciaID} deleted successfully"
        }
    except HTTPException as e:
        raise e
    
