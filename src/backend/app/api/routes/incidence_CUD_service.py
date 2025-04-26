from fastapi import FastAPI, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models.incidence import IncidenceCreate, IncidenceOut
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

@app.post("/incidence/create")
async def create_incidence(
    description: str = Form(...),
    type: str = Form(...),
    status: str = Form(...),
    incidence_id: int = Form(None)
):
    try:
        incidence = IncidenceCreate(
            description=description,
            type=type,
            status=status,
            incidence_id=incidence_id
        )
        result = controller.add(incidence.to_dict())
        return {
            "operation": "create",
            "data": result,
            "message": "Incidencia creada exitosamente"
        }
    except ValueError as e:
        raise HTTPException(400, detail=str(e))

@app.post("/incidence/update")
async def update_incidence(
    incidence_id: int = Form(...),
    description: str = Form(...),
    type: str = Form(...),
    status: str = Form(...)
):
    try:
        existing = controller.get_by_id(IncidenceOut, incidence_id)
        if not existing:
            raise HTTPException(404, detail="Incidencia no encontrada")
        
        updated = IncidenceCreate(
            incidence_id=incidence_id,
            description=description,
            type=type,
            status=status
        )
        result = controller.update(updated.to_dict())
        return {
            "operation": "update",
            "data": result,
            "message": f"Incidencia {incidence_id} actualizada"
        }
    except ValueError as e:
        raise HTTPException(400, detail=str(e))

@app.post("/incidence/delete")
async def delete_incidence(incidence_id: int = Form(...)):
    existing = controller.get_by_id(IncidenceOut, incidence_id)
    if not existing:
        raise HTTPException(404, detail="Incidencia no encontrada")
    
    controller.delete(existing)
    return {
        "operation": "delete",
        "message": f"Incidencia {incidence_id} eliminada"
    }

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8001, reload=True)