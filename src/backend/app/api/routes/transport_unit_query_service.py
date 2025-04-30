from fastapi import FastAPI, HTTPException, APIRouter, Depends
from typing import List
from backend.app.models.transport import TransportOut
from backend.app.logic.universal_controller_sql import UniversalController
import uvicorn

app = APIRouter(prefix="/transports", tags=["Transports"])
controller = UniversalController()

@app.get("/", response_model=List[TransportOut])
async def get_all_transports():
    """Obtiene todos los registros de transporte."""
    try:
        transports = controller.get_all(TransportOut)
        return transports
    except Exception as e:
        raise HTTPException(500, detail=f"Error interno del servidor: {str(e)}")

@app.get("/{transport_id}", response_model=TransportOut)
async def get_transport_by_id(transport_id: str):
    """Obtiene un registro de transporte por su ID."""
    transport = controller.get_by_id(TransportOut, transport_id)
    if transport:
        return transport
    else:
        raise HTTPException(404, detail=f"Transporte con ID {transport_id} no encontrado")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8004, reload=True)