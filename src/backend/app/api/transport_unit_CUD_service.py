from fastapi import FastAPI, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from src.backend.app.models.transport import TransportCreate, TransportOut
from logic.universal_controller_sql import UniversalController
import uvicorn
app = FastAPI()
controller = UniversalController()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/transport/unit/create")
async def create_unit(
    id: str = Form(...),
    type: str = Form(...),
    status: str = Form(...),
    ubication: str = Form(...),
    capacity: int = Form(...)
):
    try:
        transport = TransportCreate(
            id=id, type=type, status=status,
            ubication=ubication, capacity=capacity
        )
        result = controller.add(transport)
        return {"operation": "create", "data": result}
    except ValueError as e:
        raise HTTPException(400, detail=str(e))

@app.post("/transport/unit/update")
async def update_unit(
    id: str = Form(...),
    type: str = Form(...),
    status: str = Form(...),
    ubication: str = Form(...),
    capacity: int = Form(...)
):
    existing = controller.get_by_id(TransportOut, id)
    if not existing:
        raise HTTPException(404, detail="Unidad no encontrada")
    
    transport = TransportCreate(
        id=id, type=type, status=status,
        ubication=ubication, capacity=capacity
    )
    controller.update(transport)
    return {"operation": "update", "id": id}

@app.post("/transport/unit/delete")
async def delete_unit(id: str = Form(...)):
    existing = controller.get_by_id(TransportOut, id)
    if not existing:
        raise HTTPException(404, detail="Unidad no encontrada")
    
    controller.delete(existing)
    return {"operation": "delete", "id": id}
if __name__ == "__main__":
    uvicorn.run(
        app="app:app",
        host="0.0.0.0",
        port=8001,  
        reload=True
    )