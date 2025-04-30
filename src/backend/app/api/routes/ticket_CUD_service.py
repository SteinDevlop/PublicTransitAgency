from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from models import TicketCreate, TicketOut
from logic.universal_controller_sql import UniversalController
import uvicorn

app = FastAPI()
controller = UniversalController()
templates = Jinja2Templates(directory="templates")

# Configuración CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Endpoints GET para formularios HTML
@app.get("/ticket/crear", response_class=HTMLResponse, tags=["ticket"])
def show_create_form(request: Request):
    return templates.TemplateResponse("CrearTicket.html", {"request": request})

@app.get("/ticket/actualizar", response_class=HTMLResponse, tags=["ticket"])
def show_update_form(request: Request):
    return templates.TemplateResponse("ActualizarTicket.html", {"request": request})

@app.get("/ticket/eliminar", response_class=HTMLResponse, tags=["ticket"])
def show_delete_form(request: Request):
    return templates.TemplateResponse("EliminarTicket.html", {"request": request})

# Endpoints POST para operaciones
@app.post("/ticket/create", response_model=TicketOut, tags=["ticket"])
async def create_ticket(
    ticket_id: str = Form(...),
    status_code: int = Form(...),
):
    try:
        if status_code not in (1, 2, 3):
            raise ValueError("El código de estado debe ser 1, 2 o 3.")
        
        new_ticket = TicketCreate(
            ID=ticket_id,
            status_code=status_code
        )
        result = controller.add(new_ticket.to_dict())
        return TicketOut(
            ticket_id=result["ticket_id"],
            status_code=result["status_code"]
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@app.post("/ticket/update", response_model=TicketOut, tags=["ticket"])
async def update_ticket(
    ticket_id: str = Form(...),
    status_code: int = Form(...),
):
    try:
        existing_ticket = controller.get_by_id(TicketOut, ticket_id)
        if not existing_ticket:
            raise HTTPException(status_code=404, detail="Ticket no encontrado.")
        
        updated_ticket = TicketCreate(
            ID=ticket_id,
            status_code=status_code
        )
        result = controller.update(updated_ticket.to_dict())
        return TicketOut(
            ticket_id=result["ticket_id"],
            status_code=result["status_code"]
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/ticket/delete", tags=["ticket"])
async def delete_ticket(ticket_id: str = Form(...)):
    try:
        existing_ticket = controller.get_by_id(TicketOut, ticket_id)
        if not existing_ticket:
            raise HTTPException(status_code=404, detail="Ticket no encontrado.")
        
        controller.delete(existing_ticket)
        return {"message": f"Ticket {ticket_id} eliminado correctamente."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)
