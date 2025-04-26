from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from models.stops import StopCreate, StopOut
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

@app.post("/stops/create")
async def create_stop(request: Request):
    try:
        data = await request.json()
        
        if "stop_id" not in data:
            raise ValueError("stop_id is required")
        
        stop = StopCreate(
            stop_id=data['stop_id'],
            stop_data=data
        )
        
        result = controller.add(stop.to_dict())
        return {
            "operation": "create",
            "success": True,
            "data": result,
            "message": "Stop created successfully"
        }
    except ValueError as e:
        raise HTTPException(400, detail=str(e))
    except Exception as e:
        raise HTTPException(500, detail="Internal server error")

@app.post("/stops/update")
async def update_stop(request: Request):
    try:
        data = await request.json()
        
        if "stop_id" not in data:
            raise ValueError("stop_id is required")
        
        existing = controller.get_by_id(StopOut, data['stop_id'])
        if not existing:
            raise HTTPException(404, detail="Stop not found")
        
        updated = StopCreate(
            stop_id=data['stop_id'],
            stop_data=data
        )
        
        result = controller.update(updated.to_dict())
        return {
            "operation": "update",
            "success": True,
            "data": result,
            "message": f"Stop {data['stop_id']} updated"
        }
    except ValueError as e:
        raise HTTPException(400, detail=str(e))

@app.post("/stops/delete")
async def delete_stop(request: Request):
    try:
        data = await request.json()
        
        if "stop_id" not in data:
            raise ValueError("stop_id is required")
        
        existing = controller.get_by_id(StopOut, data['stop_id'])
        if not existing:
            raise HTTPException(404, detail="Stop not found")
        
        controller.delete(existing)
        return {
            "operation": "delete",
            "success": True,
            "message": f"Stop {data['stop_id']} deleted"
        }
    except Exception as e:
        raise HTTPException(500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8007, reload=True)