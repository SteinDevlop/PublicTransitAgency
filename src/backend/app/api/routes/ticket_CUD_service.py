from fastapi import FastAPI, Form, HTTPException, CORSMiddleware
from models import TicketCreate
from logic.universal_controller_sql import UniversalController
import uvicorn

app = FastAPI()
controller = UniversalController()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST"],
    allow_headers=["*"],
)

@app.post("/tickets/create")
async def create_ticket(
    status_code: int = Form(...),
    ticket_id: str = Form(...)
):
    try:
        if status_code not in (1, 2, 3):
            raise ValueError("Código de estado debe ser 1, 2 o 3")
        
        ticket = TicketCreate(status_code=status_code, ID=ticket_id)
        result = controller.add(ticket.to_dict())
        
        return {
            "operation": "create",
            "data": result,
            "message": f"Ticket {ticket_id} creado"
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8001, reload=True)