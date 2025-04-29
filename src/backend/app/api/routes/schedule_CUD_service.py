from fastapi import FastAPI, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from models.schedule import ScheduleCreate, ScheduleOut
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

@app.post("/schedule/create")
async def create_schedule(
    schedule_id: str = Form(...),
    arrival_date: str = Form(...),
    departure_date: str = Form(...),
    route: str = Form(...)
):
    try:
        schedule = ScheduleCreate(
            schedule_id=schedule_id,
            arrival_date=datetime.fromisoformat(arrival_date),
            departure_date=datetime.fromisoformat(departure_date),
            route=route
        )
        result = controller.add(schedule.to_dict())
        return {
            "operation": "create",
            "success": True,
            "data": result,
            "message": "Schedule created successfully"
        }
    except ValueError as e:
        raise HTTPException(400, detail=str(e))
    except Exception as e:
        raise HTTPException(500, detail="Internal server error")

@app.post("/schedule/update")
async def update_schedule(
    schedule_id: str = Form(...),
    arrival_date: str = Form(...),
    departure_date: str = Form(...),
    route: str = Form(...)
):
    try:
        existing = controller.get_by_id(ScheduleOut, schedule_id)
        if not existing:
            raise HTTPException(404, detail="Schedule not found")
        
        updated = ScheduleCreate(
            schedule_id=schedule_id,
            arrival_date=datetime.fromisoformat(arrival_date),
            departure_date=datetime.fromisoformat(departure_date),
            route=route
        )
        result = controller.update(updated.to_dict())
        return {
            "operation": "update",
            "success": True,
            "data": result,
            "message": f"Schedule {schedule_id} updated"
        }
    except ValueError as e:
        raise HTTPException(400, detail=str(e))

@app.post("/schedule/delete")
async def delete_schedule(schedule_id: str = Form(...)):
    try:
        existing = controller.get_by_id(ScheduleOut, schedule_id)
        if not existing:
            raise HTTPException(404, detail="Schedule not found")
        
        controller.delete(existing)
        return {
            "operation": "delete",
            "success": True,
            "message": f"Schedule {schedule_id} deleted"
        }
    except Exception as e:
        raise HTTPException(500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8003, reload=True)
