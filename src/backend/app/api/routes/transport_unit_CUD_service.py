from fastapi import FastAPI, Form, HTTPException, APIRouter, Request, Depends, HTMLResponse
from fastapi.templating import Jinja2Templates
from backend.app.models.transport import TransportCreate, TransportOut
from backend.app.logic.universal_controller_sql import UniversalController
import uvicorn

app = APIRouter(prefix="/transports", tags=["Transports"])
controller = UniversalController()

templates = Jinja2Templates(directory="src/backend/app/templates")

# Endpoints GET para formularios HTML
@app.get("/crear", response_class=HTMLResponse, tags=["transports"])
def show_create_form(request: Request):
    return templates.TemplateResponse("CrearTransport.html", {"request": request})

@app.get("/actualizar", response_class=HTMLResponse, tags=["transports"])
def show_update_form(request: Request):
    return templates.TemplateResponse("ActualizarTransport.html", {"request": request})

@app.get("/eliminar", response_class=HTMLResponse, tags=["transports"])
def show_delete_form(request: Request):
    return templates.TemplateResponse("EliminarTransport.html", {"request": request})

# Endpoints POST para operaciones
@app.post("/create", response_model=TransportOut, tags=["transports"])
async def create_transport(
    id: str = Form(...),
    type: str = Form(...),
    status: str = Form(...),
    ubication: str = Form(...),
    capacity: int = Form(...)
):
    try:
        new_transport = TransportCreate(
            id=id,
            type=type,
            status=status,
            ubication=ubication,
            capacity=capacity
        )
        result = controller.add(new_transport)
        return TransportOut(
            id=result.id,
            type=result.type,
            status=result.status,
            ubication=result.ubication,
            capacity=result.capacity
        )
    except ValueError as e:
        raise HTTPException(400, detail=str(e))
    except Exception as e:
        raise HTTPException(500, detail=f"Error interno del servidor: {str(e)}")

@app.post("/update", response_model=TransportOut, tags=["transports"])
async def update_transport(
    id: str = Form(...),
    type: str = Form(...),
    status: str = Form(...),
    ubication: str = Form(...),
    capacity: int = Form(...)
):
    try:
        existing = controller.get_by_id(TransportOut, id)
        if not existing:
            raise HTTPException(404, detail="Transporte no encontrado")

        updated_transport = TransportCreate(
            id=id,
            type=type,
            status=status,
            ubication=ubication,
            capacity=capacity
        )
        result = controller.update(updated_transport)
        return TransportOut(
            id=result.id,
            type=result.type,
            status=result.status,
            ubication=result.ubication,
            capacity=result.capacity
        )
    except ValueError as e:
        raise HTTPException(400, detail=str(e))
    except Exception as e:
        raise HTTPException(500, detail=str(e))

@app.post("/delete", tags=["transports"])
async def delete_transport(id: str = Form(...)):
    try:
        existing = controller.get_by_id(TransportOut, id)
        if not existing:
            raise HTTPException(404, detail="Transporte no encontrado")

        controller.delete(existing)
        return {"message": f"Transporte con ID {id} eliminado correctamente"}
    except Exception as e:
        raise HTTPException(500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8003, reload=True)