from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from models.stops import StopOut
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

@app.get("/stops")
async def get_all_stops():
    dummy = StopOut.get_empty_instance()
    stops = controller.read_all(dummy)
    return {"data": stops}

@app.get("/stops/{stop_id}")
async def get_stop(stop_id: str):
    stop = controller.get_by_id(StopOut, stop_id)
    if not stop:
        raise HTTPException(404, detail="Stop not found")
    return {"data": stop}

@app.get("/stops/search")
async def search_stops(
    name: str = Query(None),
    location: str = Query(None)
):
    dummy = StopOut.get_empty_instance()
    all_stops = controller.read_all(dummy)
    
    filtered = []
    for stop in all_stops:
        stop_data = stop['stop_data']
        matches = True
        if name and name.lower() not in stop_data.get('name', '').lower():
            matches = False
        if location and location.lower() not in stop_data.get('location', '').lower():
            matches = False
        if matches:
            filtered.append(stop)
    
    return {"data": filtered}

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8008, reload=True)