from fastapi import FastAPI, Form, HTTPException, APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from backend.app.models.incidence import IncidenceCreate, IncidenceOut
from backend.app.logic.universal_controller_sql import UniversalController

app = APIRouter(prefix="/incidence", tags=["incidence"])
controller = UniversalController()
templates = Jinja2Templates(directory="src/backend/app/templates")

@app.get("/crear", response_class=HTMLResponse)
def index_create(request: Request):
    """Displays the form to create a new incidence."""
    return templates.TemplateResponse("CrearIncidencia.html", {"request": request})

@app.get("/actualizar", response_class=HTMLResponse)
def index_update(request: Request):
    """Displays the form to update an existing incidence."""
    return templates.TemplateResponse("ActualizarIncidencia.html", {"request": request})

@app.get("/borrar", response_class=HTMLResponse)
def index_delete(request: Request):
    """Displays the form to delete an existing incidence."""
    return templates.TemplateResponse("EliminarIncidencia.html", {"request": request})

@app.post("/create")
async def create_incidence(
    Descripcion: str = Form(...),
    Tipo: str = Form(None),
    TicketID: int = Form(...)
):
    """Creates a new incidence."""
    try:
        new_incidence = IncidenceCreate(
            Descripcion=Descripcion,
            Tipo=Tipo,
            TicketID=TicketID
        )
        result = controller.add(new_incidence)
        return {
            "operation": "create",
            "success": True,
            "data": IncidenceOut(
                IncidenciaID=result.IncidenciaID,
                Descripcion=result.Descripcion,
                Tipo=result.Tipo,
                TicketID=result.TicketID
            ).dict(),
            "message": "Incidence created successfully"
        }
    except ValueError as e:
        raise HTTPException(400, detail=str(e))
    except Exception as e:
        raise HTTPException(500, detail=f"Internal server error: {str(e)}")

@app.post("/update")
async def update_incidence(
    IncidenciaID: int = Form(...),
    Descripcion: str = Form(...),
    Tipo: str = Form(None),
    TicketID: int = Form(...)
):
    """Updates an existing incidence."""
    try:
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
    except Exception as e:
        raise HTTPException(500, detail=f"Internal server error: {str(e)}")

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
    except Exception as e:
        raise HTTPException(500, detail=str(e))