import pytest
from fastapi.testclient import TestClient
from backend.app.api.routes.planificador_service import app as planificador_router
from fastapi import FastAPI
from backend.app.core.conf import headers
app_for_test = FastAPI()
app_for_test.include_router(planificador_router)
client = TestClient(app_for_test)

def get_token():
    # Simula un token válido para pruebas (ajusta según tu sistema de auth real)
    return "testtoken"

@pytest.mark.parametrize(
    "origen,destino,espera_exito",
    [
        ("Olimpica 13 de Junio", "Av. Universitaria y Calle 12", True),
        ("NoExiste", "Calle 12", False),
        ("Olimpica", "NoExiste", False),
    ]
)
def test_planificador_ubicaciones(origen, destino, espera_exito):
    token = get_token()
    all_headers = {"Authorization": f"Bearer {token}"}
    all_headers.update(headers)
    response = client.post(
        "/planificador/ubicaciones",
        data={"ubicacion_entrada": origen, "ubicacion_final": destino},
        headers=all_headers
    )
    if espera_exito:
        assert response.status_code == 200
        data = response.json()
        assert data is not None
        assert 'interconexiones' in data or 'ruta_inicial' in data
    else:
        # Puede ser 200 con resultado vacío, 404/400, o un mensaje de error
        assert response.status_code in (200, 400, 404)
        if response.status_code == 200:
            data = response.json()
            assert (
                not data
                or data == {}
                or data.get('interconexiones') == []
                or 'mensaje' in data  # <-- acepta mensaje de error
            )
