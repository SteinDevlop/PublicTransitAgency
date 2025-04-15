from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from datetime import datetime
from uuid import uuid4

from logic.payments import Payments
from logic.universal_controller_json import UniversalController
from logic.card import Card  

app = FastAPI()
controller = UniversalController()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuración de límites de transacción
MIN_VALOR = 1000
MAX_VALOR = 100000

def generar_registro(id_tarjeta, tipo_transporte, tipo_pago, valor, fecha):
    # Aquí luego llamarías al microservicio de movimientos
    print(f"[LOG] Registro generado - Tarjeta: {id_tarjeta}, Transporte: {tipo_transporte}, Tipo: {tipo_pago}, Valor: {valor}, Fecha: {fecha}")
    # Puedes guardar en Payments como un registro también si deseas

@app.post('/payment/tarjeta/{id}/recarga')
def recharge(id: str, valor: float, tipo_transporte: str = "virtual"):
    if valor < MIN_VALOR or valor > MAX_VALOR:
        raise HTTPException(status_code=400, detail=f"El valor debe estar entre {MIN_VALOR} y {MAX_VALOR}")

    tarjeta = controller.get_by_id(Card, id)
    if not tarjeta:
        raise HTTPException(status_code=404, detail="Tarjeta no encontrada")

    tarjeta.saldo += valor
    controller.update(tarjeta)

    fecha = datetime.now().isoformat()
    pago = Payments(str(uuid4()), id, tipo_transporte, "recarga", valor, fecha)
    controller.add(pago)

    generar_registro(id, tipo_transporte, "recarga", valor, fecha)

    return {"mensaje": "Recarga exitosa", "nuevo_saldo": tarjeta.saldo}


if __name__ == "__main__":
    uvicorn.run("app:app", reload=True)

#Da un error en payments.py que en payments.py no existe, que mamada.