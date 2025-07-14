from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from datetime import datetime
import httpx
import json
import asyncio
from pydantic import BaseModel

app = FastAPI()

WEBHOOK_URL = "https://webhook.site/db676ba8-962e-4e5b-86e2-9f7da048c4fe"
HEADERS = {"Content-Type": "application/json"}

#Servir archivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")


class Subscription(BaseModel):
    username: str
    monthly_fee: float
    start_date: datetime


#Página HTML en la raíz
@app.get("/", response_class=HTMLResponse)
async def home():
    with open("static/index.html", "r", encoding="utf-8") as f:
        return f.read()


#Envío del webhook
@app.post("/new-subscription")
async def new_subscription(body: Subscription):
    asyncio.create_task(send_webhooks(body))
    return {"mensaje": "Envío iniciado en segundo plano."}


# Lógica de envío controlado
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
                print(f"Envío #{i} - Estado: {response.status_code}")
            except httpx.RequestError as e:
                print(f"Error en envío #{i}: {str(e)}")

            await asyncio.sleep(intervalo)