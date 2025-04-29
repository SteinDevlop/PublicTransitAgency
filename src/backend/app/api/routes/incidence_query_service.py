from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from backend.app.models.incidence import IncidenceCreate, IncidenceOut
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

def build_html_response(title: str, message: str) -> HTMLResponse:
    content = f"""
    <html>
        <head><title>{title}</title></head>
        <body>
            <h1>{title}</h1>
            <p>{message}</p>
            <a href="/">Volver al inicio</a>
        </body>
    </html>
    """
    return HTMLResponse(content=content)

@app.post("/incidence/create", response_class=JSONResponse)
async def create_incidence(
    request: Request,
    description: str = Form(...),
    type: str = Form(...),
    status: str = Form(...),
    incidence_id: int = Form(None)
):
    try:
        incidence = IncidenceCreate(
            description=description,
            type=type,
            status=status,
            incidence_id=incidence_id
        )
        result = controller.add(incidence.to_dict())

        if "text/html" in request.headers.get("accept", ""):
            return build_html_response(
                "Incidencia Creada",
                f"La incidencia '{description}' fue creada exitosamente."
            )
        
        return {
            "operation": "create",
            "data": result,
            "message": "Incidencia creada exitosamente"
        }
    except ValueError as e:
        raise HTTPException(400, detail=str(e))

@app.post("/incidence/update", response_class=JSONResponse)
async def update_incidence(
    request: Request,
    incidence_id: int = Form(...),
    description: str = Form(...),
    type: str = Form(...),
    status: str = Form(...)
):
    try:
        existing = controller.get_by_id(IncidenceOut, incidence_id)
        if not existing:
            raise HTTPException(404, detail="Incidencia no encontrada")
        
        updated = IncidenceCreate(
            incidence_id=incidence_id,
            description=description,
            type=type,
            status=status
        )
        result = controller.update(updated.to_dict())

        if "text/html" in request.headers.get("accept", ""):
            return build_html_response(
                "Incidencia Actualizada",
                f"La incidencia {incidence_id} fue actualizada correctamente."
            )

        return {
            "operation": "update",
            "data": result,
            "message": f"Incidencia {incidence_id} actualizada"
        }
    except ValueError as e:
        raise HTTPException(400, detail=str(e))

@app.post("/incidence/delete", response_class=JSONResponse)
async def delete_incidence(
    request: Request,
    incidence_id: int = Form(...)
):
    existing = controller.get_by_id(IncidenceOut, incidence_id)
    if not existing:
        raise HTTPException(404, detail="Incidencia no encontrada")
    
    controller.delete(existing)

    if "text/html" in request.headers.get("accept", ""):
        return build_html_response(
            "Incidencia Eliminada",
            f"La incidencia {incidence_id} fue eliminada exitosamente."
        )

    return {
        "operation": "delete",
        "message": f"Incidencia {incidence_id} eliminada"
    }

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8001, reload=True)
