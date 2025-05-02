from fastapi import FastAPI, HTTPException, Request, Query, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from backend.app.models.ticket import TicketOut  # Asegúrate de que TicketOut exista
from backend.app.logic.universal_controller_sql import UniversalController
import uvicorn

# Initialize the FastAPI router for the "ticket" functionality
app = APIRouter(prefix="/tickets", tags=["tickets"])

controller = UniversalController()
templates = Jinja2Templates(directory="src/backend/app/templates")

@app.get("/", response_class=HTMLResponse)
def listar_tickets(request: Request):
    """Renderiza la página para consultar tickets."""
    tickets = controller.read_all(TicketOut(ticket_id=0, status_code=0))
    return templates.TemplateResponse("ConsultarTickets.html", {"request": request, "tickets": tickets})

@app.get("/{ticket_id}", response_class=HTMLResponse)
def detalle_ticket(ticket_id: int, request: Request):
    """Obtiene un ticket por su ID y lo muestra en HTML."""
    ticket = controller.get_by_id(TicketOut, ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket no encontrado")
    return templates.TemplateResponse("DetalleTicket.html", {"request": request, "ticket": ticket})

if __name__ == "__main__":
    app_main = FastAPI()
    app_main.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["GET"],
        allow_headers=["*"],
    )
    app_main.include_router(app)
    uvicorn.run(app_main, host="0.0.0.0", port=8002)