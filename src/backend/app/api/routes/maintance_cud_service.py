from fastapi import FastAPI, Form, Request, status,Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from logic.mantainment import Maintenance
from logic.universal_controller_sql import UniversalController
from datetime import datetime

app = FastAPI()
controller = UniversalController()
templates = Jinja2Templates(directory="templates")

# Middleware for CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Combined route with query parameter to load different pages
@app.get("/crear", response_class=HTMLResponse)
def crear_mantenimiento(request: Request):
    return templates.TemplateResponse("CrearMantenimiento.html", {"request": request})

@app.get("/eliminar", response_class=HTMLResponse)
def eliminar_mantenimiento(request: Request):
    return templates.TemplateResponse("EliminarMantenimiento.html", {"request": request})

@app.get("/actualizar", response_class=HTMLResponse)
def actualizar_mantenimiento(request: Request):
    return templates.TemplateResponse("ActualizarMantenimiento.html", {"request": request})
# Add mantainment
@app.post("/mantainment")
def add(
    id: int = Form(...),
    id_unit: int = Form(...),
    id_status: int = Form(...),
    type: str = Form(...),
    date: datetime = Form(...)
):
    mantainment_temp = Maintenance(id, id_unit, id_status, type, date)
    return controller.add(mantainment_temp)

# Update mantainment
@app.post("/mantainment/")
def update(
    id: int = Form(...),
    id_unit: int = Form(...),
    id_status: int = Form(...),
    type: str = Form(...),
    date: datetime = Form(...)
):
    mantainment_temp = Maintenance(id, id_unit, id_status, type, date)
    return controller.update(mantainment_temp)

# Delete mantainment
@app.post("/mantainment/eliminar")
def delete_mantainment(id: int = Form(...)):
    mantainment_temp = Maintenance(id)
    controller.delete(mantainment_temp)
    return controller.delete(mantainment_temp)
