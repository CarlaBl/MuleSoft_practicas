from datetime import datetime
import requests
import json
import asyncio

from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel

app = FastAPI()

# URL del webhook destino 
WEBHOOK_URL = "https://webhook.site/db676ba8-962e-4e5b-86e2-9f7da048c4fe"
HEADERS = {"Content-Type": "application/json"}


class Subscription(BaseModel):
    username: str
    monthly_fee: float
    start_date: datetime

#funcion asíncrona para enviar el webhook cada 5 segundos
async def send_webhook(body: Subscription):
    contador = 1
    while True:
        payload = {
            "mensaje": "Hola desde Python",
            "usuario": body.username,
            "numero_envio": contador,
            "timestamp": datetime.now().isoformat(),
            "cuota_mensual": body.monthly_fee,
            "fecha_inicio": body.start_date.isoformat()
        }

        response = requests.post(WEBHOOK_URL, data=json.dumps(payload), headers=HEADERS)
        tiempo_actual = datetime.now().strftime('%H:%M:%S')
        print(f" Envío #{contador} - Estado: {response.status_code} - Hora: {tiempo_actual}")
        contador += 1
        await asyncio.sleep(5)  # Esperar 5 segundos

# Endpoint para iniciar el envío de webhooks en segundo plano
@app.post("/new-subscription")
async def new_subscription(body: Subscription, background_tasks: BackgroundTasks):
    background_tasks.add_task(send_webhook, body)
    return {"mensaje": "Se hizo una nueva subscription."}

# Endpoint de ejemplo para verificar usuarios
@app.get("/users/")
def read_users():
    return ["Rick", "Morty"]