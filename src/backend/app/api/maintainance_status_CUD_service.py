from fastapi import FastAPI, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models.maintainance_status import MaintainanceStatusCreate, MaintainanceStatusOut
from logic.universal_controller_sql import UniversalController
import uvicorn

app = FastAPI()
controller = UniversalController()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["POST"],  
    allow_headers=["*"],
)

@app.post("/maintainance_status/create")
async def create_status(
    id: int = Form(...),
    unit: str = Form(...),
    type: str = Form(...),
    status: str = Form(...)
):
    try:
        new_status = MaintainanceStatusCreate(
            id=id,
            unit=unit,
            type=type,
            status=status
        )
        result = controller.add(new_status.to_dict())
        return {
            "operation": "create",
            "success": True,
            "data": result,
            "message": "Estado de mantenimiento creado correctamente"
        }
    except ValueError as e:
        raise HTTPException(400, detail=str(e))
    except Exception as e:
        raise HTTPException(500, detail="Error interno del servidor")

@app.post("/maintainance_status/update")
async def update_status(
    id: int = Form(...),
    unit: str = Form(...),
    type: str = Form(...),
    status: str = Form(...)
):
    try:
        existing = controller.get_by_id(MaintainanceStatusOut, id)
        if not existing:
            raise HTTPException(404, detail="Registro no encontrado")
        
        updated_status = MaintainanceStatusCreate(
            id=id,
            unit=unit,
            type=type,
            status=status
        )
        result = controller.update(updated_status.to_dict())
        
        return {
            "operation": "update",
            "success": True,
            "data": result,
            "message": f"Estado {id} actualizado correctamente"
        }
    except ValueError as e:
        raise HTTPException(400, detail=str(e))

@app.post("/maintainance_status/delete")
async def delete_status(id: int = Form(...)):
    try:
        existing = controller.get_by_id(MaintainanceStatusOut, id)
        if not existing:
            raise HTTPException(404, detail="Registro no encontrado")
        
        controller.delete(existing)
        return {
            "operation": "delete",
            "success": True,
            "message": f"Estado {id} eliminado correctamente"
        }
    except Exception as e:
        raise HTTPException(500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8001,  
        reload=True
    )