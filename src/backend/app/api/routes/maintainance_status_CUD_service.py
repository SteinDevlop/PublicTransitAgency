from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from models.maintainance_status import MaintainanceStatusCreate, MaintainanceStatusOut
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

def is_html_request(request: Request) -> bool:
    return "html" in request.headers.get("Accept", "").lower()

@app.post("/maintainance_status/create", response_class=HTMLResponse)
async def create_status(
    request: Request,
    id: int = Form(...),
    unit: str = Form(...),
    type: str = Form(...),
    status: str = Form(...)
):
    try:
        new_status = MaintainanceStatusCreate(
            id=id,
            unit=unit,
            type=type,
            status=status
        )
        result = controller.add(new_status.to_dict())
        if is_html_request(request):
            return HTMLResponse(content=f"<html><body><h1>Estado de Mantenimiento Creado</h1><p>ID: {result['id']}</p></body></html>")
        return {
            "operation": "create",
            "success": True,
            "data": result,
            "message": "Estado de mantenimiento creado correctamente"
        }
    except ValueError as e:
        raise HTTPException(400, detail=str(e))
    except Exception as e:
        raise HTTPException(500, detail="Error interno del servidor")

@app.post("/maintainance_status/update", response_class=HTMLResponse)
async def update_status(
    request: Request,
    id: int = Form(...),
    unit: str = Form(...),
    type: str = Form(...),
    status: str = Form(...)
):
    try:
        existing = controller.get_by_id(MaintainanceStatusOut, id)
        if not existing:
            raise HTTPException(404, detail="Registro no encontrado")
        
        updated_status = MaintainanceStatusCreate(
            id=id,
            unit=unit,
            type=type,
            status=status
        )
        result = controller.update(updated_status.to_dict())

        if is_html_request(request):
            return HTMLResponse(content=f"<html><body><h1>Estado Actualizado</h1><p>ID: {result['id']}</p></body></html>")
        
        return {
            "operation": "update",
            "success": True,
            "data": result,
            "message": f"Estado {id} actualizado correctamente"
        }
    except ValueError as e:
        raise HTTPException(400, detail=str(e))

@app.post("/maintainance_status/delete", response_class=HTMLResponse)
async def delete_status(request: Request, id: int = Form(...)):
    try:
        existing = controller.get_by_id(MaintainanceStatusOut, id)
        if not existing:
            raise HTTPException(404, detail="Registro no encontrado")
        
        controller.delete(existing)

        if is_html_request(request):
            return HTMLResponse(content=f"<html><body><h1>Estado Eliminado</h1><p>ID: {id}</p></body></html>")
        
        return {
            "operation": "delete",
            "success": True,
            "message": f"Estado {id} eliminado correctamente"
        }
    except Exception as e:
        raise HTTPException(500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8001,
        reload=True
    )
