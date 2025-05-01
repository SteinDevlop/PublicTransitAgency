from fastapi import FastAPI, APIRouter, Form, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from backend.app.models.stops import StopCreate, StopOut
from backend.app.logic.universal_controller_sql import UniversalController
import uvicorn

app = FastAPI()
controller = UniversalController()
templates = Jinja2Templates(directory="src/backend/app/templates")

# Configuración CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

stop_router = APIRouter(prefix="/stop", tags=["stop"])

@stop_router.get("/crear", response_class=HTMLResponse)
def crear_parada_form(request: Request):
    return templates.TemplateResponse("CrearParada.html", {"request": request})

@stop_router.post("/create")
def crear_parada(stop_id: int = Form(...), name: str = Form(...), location: str = Form(...)):
    stop_data = {"name": name, "location": location}
    parada = StopCreate(stop_id=stop_id, stop_data=stop_data)
    try:
        controller.add(parada)
        return RedirectResponse("/stops", status_code=303)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@stop_router.get("/actualizar", response_class=HTMLResponse)
def actualizar_parada_form(request: Request):
    return templates.TemplateResponse("ActualizarParada.html", {"request": request})

@stop_router.post("/update")
def actualizar_parada(stop_id: int = Form(...), name: str = Form(...), location: str = Form(...)):
    stop_data = {"name": name, "location": location}
    parada = StopCreate(stop_id=stop_id, stop_data=stop_data)
    try:
        controller.update(parada)
        return RedirectResponse("/stops", status_code=303)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@stop_router.get("/eliminar", response_class=HTMLResponse)
def eliminar_parada_form(request: Request):
    return templates.TemplateResponse("EliminarParada.html", {"request": request})

@stop_router.post("/delete")
def eliminar_parada(stop_id: int = Form(...)):
    parada = StopCreate(stop_id=stop_id, stop_data={})
    try:
        controller.delete(parada)
        return RedirectResponse("/stops", status_code=303)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

app.include_router(stop_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8007, reload=True)
