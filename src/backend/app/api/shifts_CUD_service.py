from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from models.shift import ShiftCreate, ShiftOut
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

@app.post("/shift/create")
async def create_shift(request: Request):
    try:
        data = await request.json()
        
        shift = ShiftCreate(
            unit=data['unit'],
            start_time=datetime.fromisoformat(data['start_time']),
            end_time=datetime.fromisoformat(data['end_time']),
            driver=data['driver'],
            schedule=data['schedule']
        )
        
        result = controller.add(shift.to_dict())
        return {
            "operation": "create",
            "success": True,
            "data": result,
            "message": "Shift created successfully"
        }
    except ValueError as e:
        raise HTTPException(400, detail=str(e))
    except Exception as e:
        raise HTTPException(500, detail="Internal server error")

@app.post("/shift/update")
async def update_shift(request: Request):
    try:
        data = await request.json()
        existing = controller.get_by_id(ShiftOut, data['shift_id'])
        
        if not existing:
            raise HTTPException(404, detail="Shift not found")
        
        updated = ShiftCreate(
            unit=data['unit'],
            start_time=datetime.fromisoformat(data['start_time']),
            end_time=datetime.fromisoformat(data['end_time']),
            driver=data['driver'],
            schedule=data['schedule']
        )
        
        result = controller.update(updated.to_dict())
        return {
            "operation": "update",
            "success": True,
            "data": result,
            "message": f"Shift {data['shift_id']} updated"
        }
    except ValueError as e:
        raise HTTPException(400, detail=str(e))

@app.post("/shift/delete")
async def delete_shift(request: Request):
    try:
        data = await request.json()
        existing = controller.get_by_id(ShiftOut, data['shift_id'])
        
        if not existing:
            raise HTTPException(404, detail="Shift not found")
        
        controller.delete(existing)
        return {
            "operation": "delete",
            "success": True,
            "message": f"Shift {data['shift_id']} deleted"
        }
    except Exception as e:
        raise HTTPException(500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8005, reload=True)