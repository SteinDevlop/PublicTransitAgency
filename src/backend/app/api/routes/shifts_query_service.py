from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models.shift import ShiftOut
from logic.universal_controller_sql import UniversalController
from fastapi.responses import HTMLResponse
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

@app.get("/shift", response_class=HTMLResponse)
async def get_all_shifts():
    dummy = ShiftOut.get_empty_instance()
    shifts = controller.read_all(dummy)
    
    if not shifts:
        raise HTTPException(404, detail="No shifts found")
    
    html_content = "<html><body><h1>All Shifts</h1><ul>"
    for shift in shifts:
        html_content += f"<li>{shift}</li>"
    html_content += "</ul></body></html>"
    
    return HTMLResponse(content=html_content)

@app.get("/shift/{shift_id}", response_class=HTMLResponse)
async def get_shift(shift_id: str):
    shift = controller.get_by_id(ShiftOut, shift_id)
    if not shift:
        raise HTTPException(404, detail="Shift not found")
    
    html_content = f"<html><body><h1>Shift Details</h1><p>{shift}</p></body></html>"
    
    return HTMLResponse(content=html_content)

@app.get("/shift/driver/{driver_id}", response_class=HTMLResponse)
async def get_shifts_by_driver(driver_id: str):
    dummy = ShiftOut.get_empty_instance()
    all_shifts = controller.read_all(dummy)
    filtered = [s for s in all_shifts if s['driver_id'] == driver_id]
    
    if not filtered:
        raise HTTPException(404, detail="No shifts found for this driver")
    
    html_content = "<html><body><h1>Shifts for Driver</h1><ul>"
    for shift in filtered:
        html_content += f"<li>{shift}</li>"
    html_content += "</ul></body></html>"
    
    return HTMLResponse(content=html_content)

@app.get("/shift/unit/{unit_id}", response_class=HTMLResponse)
async def get_shifts_by_unit(unit_id: str):
    dummy = ShiftOut.get_empty_instance()
    all_shifts = controller.read_all(dummy)
    filtered = [s for s in all_shifts if s['unit_id'] == unit_id]
    
    if not filtered:
        raise HTTPException(404, detail="No shifts found for this unit")
    
    html_content = "<html><body><h1>Shifts for Unit</h1><ul>"
    for shift in filtered:
        html_content += f"<li>{shift}</li>"
    html_content += "</ul></body></html>"
    
    return HTMLResponse(content=html_content)

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8006, reload=True)
