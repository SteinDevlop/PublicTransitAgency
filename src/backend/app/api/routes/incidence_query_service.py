from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models.incidence import IncidenceOut
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

@app.get("/incidence/list")
async def list_incidences():
    dummy = IncidenceOut.get_empty_instance()
    return {"data": controller.read_all(dummy)}

@app.get("/incidence/{incidence_id}")
async def get_incidence(incidence_id: int):
    incidence = controller.get_by_id(IncidenceOut, incidence_id)
    if not incidence:
        raise HTTPException(404, detail="Incidencia no encontrada")
    return {"data": incidence}

@app.get("/incidence/unit_transport/{unit_transport_id}")
async def get_by_unit_transport(unit_transport_id: int):
    # Implementar lógica específica de filtrado si es necesario
    all_incidences = controller.read_all(IncidenceOut.get_empty_instance())
    filtered = [i for i in all_incidences if i.get("unit_transport_id") == unit_transport_id]
    
    if not filtered:
        raise HTTPException(404, detail="No se encontraron incidencias")
    return {"data": filtered}

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8002, reload=True)