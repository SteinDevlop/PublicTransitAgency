from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models.maintainance_status import MaintainanceStatusOut
from logic.universal_controller_sql import UniversalController
import uvicorn

app = FastAPI()
controller = UniversalController()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

@app.get("/maintainance_status/all")
async def get_all_maintainance_status():
    dummy = MaintainanceStatusOut.get_empty_instance()
    return {"data": controller.read_all(dummy)}

@app.get("/maintainance_status/{id}")
async def get_maintainance_status(id: int):
    status = controller.get_by_id(MaintainanceStatusOut, id)
    if not status:
        raise HTTPException(404, detail="Estado de mantenimiento no encontrado")
    return {"data": status}

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8002, reload=True)