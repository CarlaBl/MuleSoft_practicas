from datetime import datetime
import json
import asyncio
import httpx

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# URL del webhook destino 
WEBHOOK_URL = "https://webhook.site/3b286f26-8180-4267-a4b1-d00fb2b4d393"
HEADERS = {"Content-Type": "application/json"}


class Subscription(BaseModel):
    username: str
    monthly_fee: float
    start_date: datetime

#funcion asíncrona para enviar el webhook cada 5 segundos
async def send_webhooks(body: Subscription, cantidad_envios: int = 5, intervalo: int = 5):
    async with httpx.AsyncClient() as client:
        for i in range(1, cantidad_envios + 1):
            payload = {
                "mensaje": "Hola desde FastAPI",
                "usuario": body.username,
                "numero_envio": i,
                "timestamp": datetime.now().isoformat(),
                "cuota_mensual": body.monthly_fee,
                "fecha_inicio": body.start_date.isoformat()
            }

            try:
                response = await client.post(WEBHOOK_URL, data=json.dumps(payload), headers=HEADERS, timeout=5)
                print(f"Envío #{i} - Estado: {response.status_code} - Hora: {datetime.now().strftime('%H:%M:%S')}")
            except httpx.RequestError as e:
                print(f"Error al enviar webhook #{i}: {str(e)}")

            await asyncio.sleep(intervalo)

# Endpoint para iniciar el envío de webhooks en segundo plano
@app.post("/new-subscription")
async def new_subscription(body: Subscription):
    asyncio.create_task(send_webhooks(body))
    return {"mensaje": "Envíos iniciados en segundo plano."}

# Endpoint de ejemplo para verificar usuarios
@app.get("/users/")
def read_users():
    return ["Rick", "Morty"]