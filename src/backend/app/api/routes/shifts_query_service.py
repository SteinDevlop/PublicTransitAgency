from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from models.shift import ShiftOut
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

@app.get("/shift")
async def get_all_shifts():
    dummy = ShiftOut.get_empty_instance()
    shifts = controller.read_all(dummy)
    return {"data": shifts}

@app.get("/shift/{shift_id}")
async def get_shift(shift_id: str):
    shift = controller.get_by_id(ShiftOut, shift_id)
    if not shift:
        raise HTTPException(404, detail="Shift not found")
    return {"data": shift}

@app.get("/shift/driver/{driver_id}")
async def get_shifts_by_driver(driver_id: str):
    dummy = ShiftOut.get_empty_instance()
    all_shifts = controller.read_all(dummy)
    filtered = [s for s in all_shifts if s['driver_id'] == driver_id]
    
    if not filtered:
        raise HTTPException(404, detail="No shifts found for this driver")
    return {"data": filtered}

@app.get("/shift/unit/{unit_id}")
async def get_shifts_by_unit(unit_id: str):
    dummy = ShiftOut.get_empty_instance()
    all_shifts = controller.read_all(dummy)
    filtered = [s for s in all_shifts if s['unit_id'] == unit_id]
    
    if not filtered:
        raise HTTPException(404, detail="No shifts found for this unit")
    return {"data": filtered}

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8006, reload=True)
