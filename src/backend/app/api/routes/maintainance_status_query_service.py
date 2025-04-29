from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from models.maintainance_status import MaintainanceStatusOut
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

@app.get("/maintainance_status/all", response_class=HTMLResponse)
async def get_all_maintainance_status(request: Request):
    dummy = MaintainanceStatusOut.get_empty_instance()
    data = controller.read_all(dummy)

    if "html" in request.headers.get("Accept", "").lower():
        html_content = "<html><body><h1>Estados de Mantenimiento</h1><ul>"
        for item in data:
            html_content += f"<li>{item.id}: {item.name}</li>"
        html_content += "</ul></body></html>"
        return HTMLResponse(content=html_content)

    return {"data": data}

@app.get("/maintainance_status/{id}", response_class=HTMLResponse)
async def get_maintainance_status(id: int, request: Request):
    status = controller.get_by_id(MaintainanceStatusOut, id)
    if not status:
        raise HTTPException(404, detail="Estado de mantenimiento no encontrado")

    if "html" in request.headers.get("Accept", "").lower():
        html_content = f"<html><body><h1>Estado de Mantenimiento {id}</h1>"
        html_content += f"<p>{status.id}: {status.name}</p></body></html>"
        return HTMLResponse(content=html_content)

    return {"data": status}

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8002, reload=True)
