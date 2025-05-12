from fastapi import APIRouter, HTTPException, Request, Security
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from backend.app.logic.universal_controller_sqlserver import UniversalController
from backend.app.models.stops import Parada
from backend.app.core.auth import get_current_user

app = APIRouter(prefix="/stops", tags=["stops"])
controller = UniversalController()
templates = Jinja2Templates(directory="src/backend/app/templates")

@app.get("/", response_class=HTMLResponse)
<<<<<<< HEAD
<<<<<<< HEAD
=======
<<<<<<< HEAD
def listar_paradas(request: Request):
=======
>>>>>>> 52e45f5 (Corrections on test)
=======
>>>>>>> de23b1a (changes)
def listar_paradas(
    request: Request,
):
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> a8980fb (Corrections on test)
>>>>>>> 52e45f5 (Corrections on test)
=======
>>>>>>> de23b1a (changes)
    """
    Lista todas las paradas.
    """
    paradas = controller.read_all(Parada)
    return templates.TemplateResponse("ListarParadas.html", {"request": request, "paradas": paradas})

@app.get("/{id}", response_class=HTMLResponse)
<<<<<<< HEAD
<<<<<<< HEAD
=======
<<<<<<< HEAD
def detalle_parada(id: int, request: Request):
=======
>>>>>>> 52e45f5 (Corrections on test)
=======
>>>>>>> de23b1a (changes)
def obtener_detalle_parada(
    id: int,
    request: Request,
):
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> a8980fb (Corrections on test)
>>>>>>> 52e45f5 (Corrections on test)
=======
>>>>>>> de23b1a (changes)
    """
    Obtiene el detalle de una parada por su ID.
    """
    parada = controller.get_by_id(Parada, id)
    if not parada:
        raise HTTPException(status_code=404, detail="Parada no encontrada")
    return templates.TemplateResponse("DetalleParada.html", {"request": request, "parada": parada.to_dict()})
