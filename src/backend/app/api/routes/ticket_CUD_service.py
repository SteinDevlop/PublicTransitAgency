from fastapi import FastAPI, APIRouter, Form, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from backend.app.models.ticket import TicketCreate, TicketOut
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

ticket_router = APIRouter(prefix="/ticket", tags=["ticket"])

@ticket_router.get("/crear", response_class=HTMLResponse)
def crear_ticket_form(request: Request):
    return templates.TemplateResponse("CrearTicket.html", {"request": request})

@ticket_router.post("/create")
def crear_ticket(ticket_id: int = Form(...), status_code: int = Form(...)):
    ticket = TicketCreate(ticket_id=ticket_id, status_code=status_code)
    try:
        controller.add(ticket)
        return RedirectResponse("/tickets", status_code=303)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@ticket_router.get("/actualizar", response_class=HTMLResponse)
def actualizar_ticket_form(request: Request):
    return templates.TemplateResponse("ActualizarTicket.html", {"request": request})

@ticket_router.post("/update")
def actualizar_ticket(ticket_id: int = Form(...), status_code: int = Form(...)):
    ticket = TicketCreate(ticket_id=ticket_id, status_code=status_code)
    try:
        controller.update(ticket)
        return RedirectResponse("/tickets", status_code=303)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@ticket_router.get("/eliminar", response_class=HTMLResponse)
def eliminar_ticket_form(request: Request):
    return templates.TemplateResponse("EliminarTicket.html", {"request": request})

@ticket_router.post("/delete")
def eliminar_ticket(ticket_id: int = Form(...)):
    ticket = TicketCreate(ticket_id=ticket_id, status_code=0)
    try:
        controller.delete(ticket)
        return RedirectResponse("/tickets", status_code=303)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

app.include_router(ticket_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)