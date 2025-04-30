from fastapi import FastAPI, HTTPException, Request, Query
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
import uvicorn

from backend.app.models.ticket import TicketOut  # Modelo de ejemplo
from backend.app.logic.universal_controller_sql import UniversalController

# Initialize the FastAPI application
app = FastAPI()

# Initialize the controller to handle database operations
controller = UniversalController()

templates = Jinja2Templates(directory="src/backend/app/templates")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

# Helper to determine response type (HTML or JSON)
def _respond(data, request: Request, template: str):
    """Returns HTML or JSON based on the 'Accept' header."""
    if "text/html" in request.headers.get("Accept", ""):
        return templates.TemplateResponse(
            template,
            {"request": request, "data": data}
        )
    return JSONResponse(content={"data": data})

# Route to get all tickets
@app.get("/tickets/all", response_class=HTMLResponse)
async def get_all_tickets(
    request: Request,
    skip: int = Query(0, description="Records to skip"),
    limit: int = Query(10, description="Limit the number of results")
):
    try:
        dummy = TicketOut.get_empty_instance()
        records = controller.read_all(dummy)[skip:skip + limit]
        return _respond(records, request, "list_all.html")
    except Exception as e:
        raise HTTPException(500, detail=str(e))

# Route to get a ticket by ID
@app.get("/tickets/{ticket_id}", response_class=HTMLResponse)
async def get_ticket(
    request: Request,
    ticket_id: str = Query(..., description="Ticket ID")
):
    try:
        ticket = controller.get_by_id(TicketOut, ticket_id)
        if not ticket:
            raise HTTPException(404, detail="Ticket not found")
        return _respond(ticket, request, "detail.html")
    except Exception as e:
        raise HTTPException(500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)
