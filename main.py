from datetime import datetime
import requests
import json
import asyncio

from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel

app = FastAPI()

# URL del webhook destino (puedes modificarla)
WEBHOOK_URL = "https://webhook.site/tu-id-aquí"
HEADERS = {"Content-Type": "application/json"}


class Subscription(BaseModel):
    username: str
    monthly_fee: float
    start_date: datetime

# Función para enviar el webhook en segundo plano
async def send_webhook(body: Subscription):
    contador = 1
    while True:
        payload = {
            "mensaje": "Hola desde Python",
            "usuario": body.username,
            "tecnologia": "Webhook + JSON",
            "timestamp": datetime.now().isoformat(),
            "numero_envio": contador,
            "cuota_mensual": body.monthly_fee,
            "fecha_inicio": body.start_date.isoformat()
        }

        response = requests.post(WEBHOOK_URL, data=json.dumps(payload), headers=HEADERS)
        tiempo_actual = datetime.now().strftime('%H:%M:%S')
        print(f" Envío #{contador} - Estado: {response.status_code} - Hora: {tiempo_actual}")
        contador += 1
        await asyncio.sleep(5)  # Esperar 5 segundos

# Define la ruta para iniciar el webhook en segundo plano
@app.post("/new-subscription")
async def new_subscription(body: Subscription, background_tasks: BackgroundTasks):
    background_tasks.add_task(send_webhook, body)
    return {"mensaje": "Webhook iniciado en segundo plano."}

# Define una ruta de prueba para verificar que el servidor está funcionando
@app.get("/")
def read_root():
    return {"mensaje": "Servidor de Webhook activo"}

# Ruta de prueba para obtener una lista de usuarios
@app.get("/users/")
def read_users():
    return ["Rick", "Morty"]