from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from backend.app.models.incidence import IncidenceCreate, IncidenceOut
from logic.universal_controller_sql import UniversalController
import uvicorn

app = FastAPI(
    title="CUD Service - Incidencias",
    description="Microservicio para creación, actualización y eliminación de incidencias",
    version="1.0.0"
)

controller = UniversalController()
templates = Jinja2Templates(directory="src/backend/app/templates")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"],
)

# Formularios HTML
@app.get("/incidence/crear", response_class=HTMLResponse, tags=["incidence"])
def show_create_form(request: Request):
    return templates.TemplateResponse("CrearIncidencia.html", {"request": request})

@app.get("/incidence/actualizar", response_class=HTMLResponse, tags=["incidence"])
def show_update_form(request: Request):
    return templates.TemplateResponse("ActualizarIncidencia.html", {"request": request})

@app.get("/incidence/eliminar", response_class=HTMLResponse, tags=["incidence"])
def show_delete_form(request: Request):
    return templates.TemplateResponse("EliminarIncidencia.html", {"request": request})

# Operaciones POST
@app.post("/incidence/create", response_model=IncidenceOut, tags=["incidence"])
async def create_incidence(
    description: str = Form(...),
    type: str = Form(...),
    status: str = Form(...),
    incidence_id: int = Form(None)
):
    try:
        incidence = IncidenceCreate(
            description=description,
            type=type,
            status=status,
            incidence_id=incidence_id
        )
        result = controller.add(incidence)
        return result
    except ValueError as e:
        raise HTTPException(400, detail=str(e))

@app.post("/incidence/update", response_model=IncidenceOut, tags=["incidence"])
async def update_incidence(
    incidence_id: int = Form(...),
    description: str = Form(...),
    type: str = Form(...),
    status: str = Form(...)
):
    try:
        existing = controller.get_by_id(IncidenceOut, incidence_id)
        if not existing:
            raise HTTPException(404, detail="Incidencia no encontrada")
        
        updated = IncidenceCreate(
            incidence_id=incidence_id,
            description=description,
            type=type,
            status=status
        )
        result = controller.update(updated)
        return result
    except ValueError as e:
        raise HTTPException(400, detail=str(e))

@app.post("/incidence/delete", tags=["incidence"])
async def delete_incidence(incidence_id: int = Form(...)):
    existing = controller.get_by_id(IncidenceOut, incidence_id)
    if not existing:
        raise HTTPException(404, detail="Incidencia no encontrada")
    
    controller.delete(existing)
    return {"message": f"Incidencia {incidence_id} eliminada correctamente"}

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8001, reload=True)
