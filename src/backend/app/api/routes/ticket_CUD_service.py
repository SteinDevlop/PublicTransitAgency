from fastapi import FastAPI, Form, HTTPException, CORSMiddleware
from models import TicketCreate, TicketOut
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

@app.post("/ticket/create")
async def create_ticket(
    status_code: int = Form(...),
    ticket_id: str = Form(...)
):
    try:
        # Validación de status_code
        if status_code not in (1, 2, 3):
            raise ValueError("Código de estado debe ser 1, 2 o 3")
        
        # Crear ticket
        ticket = TicketCreate(status_code=status_code, ID=ticket_id)
        
        # Usar el controlador universal para crear el ticket
        result = controller.add(ticket.to_dict())
        
        # Devolver respuesta
        return {
            "operation": "create",
            "data": result,
            "message": f"Ticket {ticket_id} creado"
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@app.post("/ticket/update")
async def update_ticket(
    ticket_id: str = Form(...),
    status_code: int = Form(...),
):
    try:
        if status_code not in (1, 2, 3):
            raise ValueError("Código de estado debe ser 1, 2 o 3")

        existing = controller.get_by_id(TicketOut, ticket_id)
        if not existing:
            raise HTTPException(status_code=404, detail="Ticket no encontrado")
        
        ticket = TicketCreate(status_code=status_code, ID=ticket_id)
        result = controller.update(ticket.to_dict())
        
        return {
            "operation": "update",
            "data": result,
            "message": f"Ticket {ticket_id} actualizado"
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@app.post("/ticket/delete")
async def delete_ticket(ticket_id: str = Form(...)):
    try:
        existing = controller.get_by_id(TicketOut, ticket_id)
        if not existing:
            raise HTTPException(status_code=404, detail="Ticket no encontrado")
        
        controller.delete(existing)
        
        return {
            "operation": "delete",
            "message": f"Ticket {ticket_id} eliminado"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8001, reload=True)
