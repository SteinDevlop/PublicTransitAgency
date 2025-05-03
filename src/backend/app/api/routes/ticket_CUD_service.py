from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from backend.app.logic.universal_controller_sql import UniversalController
from backend.app.models.ticket import Ticket

app = APIRouter(prefix="/tickets", tags=["tickets"])
controller = UniversalController()
templates = Jinja2Templates(directory="src/backend/app/templates")

@app.get("/create", response_class=HTMLResponse)
def crear_ticket_form(request: Request):
    return templates.TemplateResponse("CrearTicket.html", {"request": request})

@app.post("/create")
def crear_ticket(ID: int = Form(...), EstadoIncidencia: str = Form(...)):
    ticket = Ticket(ID=ID, EstadoIncidencia=EstadoIncidencia)
    try:
        controller.add(ticket)
        return {
            "operation": "create",
            "success": True,
            "data": ticket,
            "message": "Ticket creado exitosamente."
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/update", response_class=HTMLResponse)
def actualizar_ticket_form(request: Request):
    return templates.TemplateResponse("ActualizarTicket.html", {"request": request})

@app.post("/update")
def actualizar_ticket(ID: int = Form(...), EstadoIncidencia: str = Form(...)):
    ticket = Ticket(ID=ID, EstadoIncidencia=EstadoIncidencia)
    try:
        controller.update(ticket)
        return {
            "operation": "update",
            "success": True,
            "data": ticket,
            "message": "Ticket actualizado exitosamente."
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/delete", response_class=HTMLResponse)
def eliminar_ticket_form(request: Request):
    return templates.TemplateResponse("EliminarTicket.html", {"request": request})

@app.post("/delete")
def eliminar_ticket(ID: int = Form(...)):
    ticket = Ticket(ID=ID, EstadoIncidencia="")
    try:
        controller.delete(ticket)
        return {
            "operation": "delete",
            "success": True,
            "message": "Ticket eliminado exitosamente."
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))