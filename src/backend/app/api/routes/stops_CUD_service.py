from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from models.stops import StopCreate, StopOut
from logic.universal_controller_sql import UniversalController
from fastapi.responses import HTMLResponse
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

@app.post("/stops/create", response_class=HTMLResponse)
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
        html_content = f"""
        <html>
            <body>
                <h1>Stop Created Successfully</h1>
                <p>Operation: create</p>
                <p>Stop ID: {data['stop_id']}</p>
                <p>Message: Stop created successfully</p>
            </body>
        </html>
        """
        return HTMLResponse(content=html_content)
    except ValueError as e:
        raise HTTPException(400, detail=str(e))
    except Exception as e:
        raise HTTPException(500, detail="Internal server error")

@app.post("/stops/update", response_class=HTMLResponse)
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
        html_content = f"""
        <html>
            <body>
                <h1>Stop Updated Successfully</h1>
                <p>Operation: update</p>
                <p>Stop ID: {data['stop_id']}</p>
                <p>Message: Stop {data['stop_id']} updated</p>
            </body>
        </html>
        """
        return HTMLResponse(content=html_content)
    except ValueError as e:
        raise HTTPException(400, detail=str(e))

@app.post("/stops/delete", response_class=HTMLResponse)
async def delete_stop(request: Request):
    try:
        data = await request.json()
        
        if "stop_id" not in data:
            raise ValueError("stop_id is required")
        
        existing = controller.get_by_id(StopOut, data['stop_id'])
        if not existing:
            raise HTTPException(404, detail="Stop not found")
        
        controller.delete(existing)
        html_content = f"""
        <html>
            <body>
                <h1>Stop Deleted Successfully</h1>
                <p>Operation: delete</p>
                <p>Stop ID: {data['stop_id']}</p>
                <p>Message: Stop {data['stop_id']} deleted</p>
            </body>
        </html>
        """
        return HTMLResponse(content=html_content)
    except Exception as e:
        raise HTTPException(500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8007, reload=True)
