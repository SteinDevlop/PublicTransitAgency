from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models.schedule import ScheduleOut
from logic.universal_controller_sql import UniversalController
import uvicorn

app = FastAPI()
controller = UniversalController()

# Configuración CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

@app.get("/schedule", tags=["schedule"])
async def get_all_schedules():
    try:
        schedules = controller.read_all(ScheduleOut)
        return {
            "operation": "read_all",
            "success": True,
            "data": schedules,
            "message": "Schedules retrieved successfully"
        }
    except Exception as e:
        raise HTTPException(500, detail="Internal server error")

@app.get("/schedule/{schedule_id}", tags=["schedule"])
async def get_schedule_by_id(schedule_id: str):
    try:
        schedule = controller.get_by_id(ScheduleOut, schedule_id)
        if not schedule:
            raise HTTPException(404, detail="Schedule not found")
        return {
            "operation": "read_by_id",
            "success": True,
            "data": schedule,
            "message": f"Schedule {schedule_id} found"
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(500, detail="Internal server error")

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8003, reload=True)
