from fastapi import FastAPI, Form, HTTPException, APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from backend.app.models.transport import TransportCreate, TransportOut
from backend.app.models.transport import TransportUnitCreate
from backend.app.logic.universal_controller_sql import UniversalController
import uvicorn

app = APIRouter(prefix="/transports", tags=["transports"])
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

@app.get("/create", response_class=HTMLResponse)
def crear_unidad_form(request):
    return templates.TemplateResponse("CrearTransport.html", {"request": request})

@app.post("/create")
def crear_unidad(id: str = Form(...), type: str = Form(...), status: str = Form(...), ubication: str = Form(...), capacity: int = Form(...)):
    unidad = TransportUnitCreate(id=id, type=type, status=status, ubication=ubication, capacity=capacity)
    try:
        controller.add(unidad)
        return RedirectResponse("/transports", status_code=303)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/update", response_class=HTMLResponse)
def actualizar_unidad_form(request):
    return templates.TemplateResponse("ActualizarTransport.html", {"request": request})

@app.post("/update")
def actualizar_unidad(id: str = Form(...), type: str = Form(...), status: str = Form(...), ubication: str = Form(...), capacity: int = Form(...)):
    unidad = TransportUnitCreate(id=id, type=type, status=status, ubication=ubication, capacity=capacity)
    try:
        controller.update(unidad)
        return RedirectResponse("/transports", status_code=303)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/delete", response_class=HTMLResponse)
def eliminar_unidad_form(request):
    return templates.TemplateResponse("EliminarTransport.html", {"request": request})

@app.post("/delete")
def eliminar_unidad(id: str = Form(...)):
    unidad = TransportUnitCreate(id=id, type="", status="", ubication="", capacity=0)
    try:
        controller.delete(unidad)
        return RedirectResponse("/transports", status_code=303)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

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