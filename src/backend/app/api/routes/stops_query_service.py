from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
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

@app.get("/stops", response_class=HTMLResponse)
async def get_all_stops():
    dummy = StopOut.get_empty_instance()
    stops = controller.read_all(dummy)
    stop_list = "".join([f"<li>{stop['stop_data']['name']} - {stop['stop_data']['location']}</li>" for stop in stops])
    return f"<h1>All Stops</h1><ul>{stop_list}</ul>"

@app.get("/stops/{stop_id}", response_class=HTMLResponse)
async def get_stop(stop_id: str):
    stop = controller.get_by_id(StopOut, stop_id)
    if not stop:
        raise HTTPException(404, detail="Stop not found")
    stop_data = stop['stop_data']
    return f"<h1>Stop Details</h1><p><strong>Name:</strong> {stop_data['name']}</p><p><strong>Location:</strong> {stop_data['location']}</p>"

@app.get("/stops/search", response_class=HTMLResponse)
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
    
    if not filtered:
        return "<h1>No Stops Found</h1>"
    
    filtered_list = "".join([f"<li>{stop['stop_data']['name']} - {stop['stop_data']['location']}</li>" for stop in filtered])
    return f"<h1>Search Results</h1><ul>{filtered_list}</ul>"

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8008, reload=True)
