from fastapi import FastAPI, Request, Depends, HTTPException, Form,Path,APIRouter
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from backend.app.core.auth import encode_token, get_current_user, verify_role
from starlette.status import HTTP_302_FOUND
from fastapi.staticfiles import StaticFiles
app = APIRouter(prefix="/login", tags=["Login"])
templates = Jinja2Templates(directory="src/frontend/templates")
# Simulación de base de datos
users = {
    "122": {
        "username": "pasajero_1",
        "email": "pasajero@gmail.com",
        "password": "1234",
        "tel": "+32 123456",
        "type_card": "standard",
        "saldo": 1200,
        "scope": "pasajero"
    },
    "123": {
        "username": "admin_1",
        "email": "admin@gmail.com",
        "password": "admin1234",
        "tel": "+32 987654",
        "type_card": "none",
        "saldo": 0,
        "scope": "administrador"
    },
    "124": {
        "username": "operador_1",
        "email": "operador@gmail.com",
        "password": "op1234",
        "tel": "+32 112233",
        "type_card": "none",
        "saldo": 0,
        "scope": "operador"
    },
    "125": {
        "username": "supervisor_1",
        "email": "supervisor@gmail.com",
        "password": "sup1234",
        "tel": "+32 223344",
        "type_card": "none",
        "saldo": 0,
        "scope": "supervisor"
    },
    "126": {
        "username": "tecnico_1",
        "email": "tecnico@gmail.com",
        "password": "tec1234",
        "tel": "+32 334455",
        "type_card": "none",
        "saldo": 0,
        "scope": "tecnico"
    }
}
@app.post("/", response_model=dict)
def login_for_token(form_data: OAuth2PasswordRequestForm = Depends()):
    for user_id, user in users.items():
        if user["username"] == form_data.username and user["password"] == form_data.password:
            token = encode_token({
                "sub": user_id,
                "scope": user["scope"],
                "username": user["username"]
            })
            return {
                "access_token": token,
                "token_type": "bearer"
            }
    raise HTTPException(status_code=400, detail="Invalid credentials")
# Mostrar el formulario de inicio de sesión
@app.get("/", response_class=HTMLResponse)
def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

# Procesar el formulario de inicio de sesión
@app.post("/log")
def login_submit(
    request: Request,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    for user_id, user in users.items():
        if user["username"] == form_data.username and user["password"] == form_data.password:
            token = encode_token({"sub": user_id, "scope": user["scope"]})
            response = RedirectResponse(
                url=f"/login/user/{user['scope']}", status_code=HTTP_302_FOUND
            )
            # Puedes guardar el token en una cookie si estás usando sesiones (solo como ejemplo)
            response.set_cookie(key="access_token", value=f"Bearer {token}", httponly=True)
            return response

    raise HTTPException(status_code=400, detail="Invalid credentials")

# Mostrar el perfil del usuario (ejemplo para pasajero)
@app.get("/user/{scope}", response_class=HTMLResponse, name="user_page")
def user_page(
    request: Request,
    scope: str = Path(..., pattern="^(pasajero|administrador|operador|supervisor|tecnico)$"),
    current_user: dict = Depends(get_current_user)
):
    # Verificar que el scope del token coincida con el de la URL
    if current_user["scope"] != scope:
        raise HTTPException(status_code=403, detail="Access forbidden")

    user = users.get(current_user["user_id"])
    return templates.TemplateResponse(f"{scope}.html", {"request": request, "user": user})