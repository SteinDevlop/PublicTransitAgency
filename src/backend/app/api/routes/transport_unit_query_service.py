from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException
from models.transport import TransportOut
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

@app.get("/transport/schema")
async def get_schema():
    return {
        "name": "transport",
        "fields": [
            {"name": "id", "type": "str", "required": True},
            {"name": "type", "type": "str", "required": True},
            {"name": "status", "type": "str", "required": True},
            {"name": "ubication", "type": "str", "required": True},
            {"name": "capacity", "type": "int", "required": True}
        ]
    }

@app.get("/transport/unit/all")
async def get_all():
    dummy = TransportOut.get_empty_instance()
    return controller.read_all(dummy)

@app.get("/transport/unit/{id}")
async def get_by_id(id: str):
    unit = controller.get_by_id(TransportOut, id)
    if not unit:
        raise HTTPException(404, detail="Unidad no encontrada")
    return unit

if __name__ == "__main__":
    uvicorn.run(
        app="app:app",
        host="0.0.0.0",
        port=8002, 
        reload=True
    )