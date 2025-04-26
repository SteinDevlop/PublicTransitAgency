from fastapi import FastAPI, HTTPException, CORSMiddleware
from models import TicketOut
from logic.universal_controller_sql import UniversalController
import uvicorn

app = FastAPI()
controller = UniversalController()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

@app.get("/tickets/all")
async def get_all_tickets():
    tickets = controller.read_all(TicketOut.get_empty_instance())
    return {"tickets": tickets}

@app.get("/tickets/{ticket_id}")
async def get_ticket(ticket_id: str):
    ticket = controller.get_by_id(TicketOut, ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket no encontrado")
    return ticket

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8002, reload=True)