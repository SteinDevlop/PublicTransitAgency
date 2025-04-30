from fastapi import FastAPI, Form, HTTPException,APIRouter,Request, Depends
from fastapi.templating import Jinja2Templates
from backend.app.models.stops import StopCreate, StopOut
from backend.app.logic.universal_controller_sql import UniversalController
import uvicorn

app = APIRouter(prefix="/stops", tags=["Stops"])
controller = UniversalController()

templates = Jinja2Templates(directory="src/backend/app/templates")  # Set up the template directory

@app.post("/create")
async def create_stop(
    stop_id: str = Form(...),
    name: str = Form(...),
    location: str = Form(...)
):
    try:
        stop_data = {
            "stop_id": stop_id,
            "name": name,
            "location": location
        }
        stop = StopCreate(stop_id=stop_id, stop_data=stop_data)
        result = controller.add(stop.to_dict())
        return {
            "operation": "create",
            "success": True,
            "data": result,
            "message": "Stop created successfully"
        }
    except ValueError as e:
        raise HTTPException(400, detail=str(e))
    except Exception:
        raise HTTPException(500, detail="Internal server error")

@app.post("/update")
async def update_stop(
    stop_id: str = Form(...),
    name: str = Form(...),
    location: str = Form(...)
):
    existing = controller.get_by_id(StopOut, stop_id)
    if not existing:
        raise HTTPException(404, detail="Stop not found")
    
    stop_data = {
        "stop_id": stop_id,
        "name": name,
        "location": location
    }
    updated = StopCreate(stop_id=stop_id, stop_data=stop_data)
    result = controller.update(updated.to_dict())
    return {
        "operation": "update",
        "success": True,
        "data": result,
        "message": f"Stop {stop_id} updated"
    }

@app.post("/delete")
async def delete_stop(stop_id: str = Form(...)):
    existing = controller.get_by_id(StopOut, stop_id)
    if not existing:
        raise HTTPException(404, detail="Stop not found")
    
    controller.delete(existing)
    return {
        "operation": "delete",
        "success": True,
        "message": f"Stop {stop_id} deleted"
    }

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8007, reload=True)
