from fastapi import FastAPI, HTTPException, Request, Query, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from backend.app.models.ticket import TicketOut  # Asegúrate de que TicketOut exista
from logic.universal_controller_sql import UniversalController
import uvicorn

# Initialize the FastAPI router for the "ticket" functionality
app = APIRouter(prefix="/tickets", tags=["tickets"])

controller = UniversalController()
templates = Jinja2Templates(directory="src/backend/app/templates")

# Endpoint para la página de consulta principal (HTML)
@app.get("/consultar", response_class=HTMLResponse)
async def consultar_tickets_html(request: Request):
    """Renderiza la página para consultar tickets."""
    return templates.TemplateResponse("ConsultarTickets", {"request": request})

# Endpoint para listar todos los tickets (HTML)
@app.get("", response_class=HTMLResponse)
async def listar_tickets_html(
    request: Request,
    skip: int = Query(0, description="Registros a saltar"),
    limit: int = Query(10, description="Límite de resultados")
):
    """Lista todos los tickets en formato HTML."""
    try:
        dummy = TicketOut.get_empty_instance()
        tickets = controller.read_all(dummy)[skip:skip + limit]
        if not tickets:
            raise HTTPException(status_code=404, detail="No se encontraron tickets")
        return templates.TemplateResponse("ListarTickets", {"request": request, "tickets": tickets})
    except Exception as e:
        raise HTTPException(500, detail=str(e))

# Endpoint para listar todos los tickets (JSON)
@app.get("/json")
async def listar_tickets_json(
    skip: int = Query(0, description="Registros a saltar"),
    limit: int = Query(10, description="Límite de resultados")
):
    """Lista todos los tickets en formato JSON."""
    try:
        dummy = TicketOut.get_empty_instance()
        tickets = controller.read_all(dummy)[skip:skip + limit]
        if not tickets:
            raise HTTPException(status_code=404, detail="No se encontraron tickets")
        return JSONResponse(content={"data": [ticket.dict() for ticket in tickets]})
    except Exception as e:
        raise HTTPException(500, detail=str(e))

# Endpoint para obtener un ticket por ID (HTML)
@app.get("/{ticket_id}", response_class=HTMLResponse)
async def obtener_ticket_html(request: Request, ticket_id: str):
    """Obtiene un ticket por su ID y lo muestra en HTML."""
    try:
        ticket = controller.get_by_id(TicketOut, ticket_id)
        if not ticket:
            raise HTTPException(status_code=404, detail="Ticket no encontrado")
        return templates.TemplateResponse("DetalleTicket", {"request": request, "ticket": ticket})
    except Exception as e:
        raise HTTPException(500, detail=str(e))

# Endpoint para obtener un ticket por ID (JSON)
@app.get("/{ticket_id}/json")
async def obtener_ticket_json(ticket_id: str):
    """Obtiene un ticket por su ID en formato JSON."""
    try:
        ticket = controller.get_by_id(TicketOut, ticket_id)
        if not ticket:
            raise HTTPException(status_code=404, detail="Ticket no encontrado")
        return JSONResponse(content={"data": ticket.dict()})
    except Exception as e:
        raise HTTPException(500, detail=str(e))

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