from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models.schedule import ScheduleOut
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

@app.get("/schedule")
async def list_all_schedules():
    dummy = ScheduleOut.get_empty_instance()
    schedules = controller.read_all(dummy)
    return {"data": schedules}

@app.get("/schedule/{schedule_id}")
async def get_schedule(schedule_id: str):
    schedule = controller.get_by_id(ScheduleOut, schedule_id)
    if not schedule:
        raise HTTPException(404, detail="Schedule not found")
    return {"data": schedule}

@app.get("/schedule/route/{route_id}")
async def get_schedules_by_route(route_id: str):
    dummy = ScheduleOut.get_empty_instance()
    all_schedules = controller.read_all(dummy)
    filtered = [s for s in all_schedules if s['route_id'] == route_id]
    
    if not filtered:
        raise HTTPException(404, detail="No schedules found for this route")
    return {"data": filtered}

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8004, reload=True)