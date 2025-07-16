from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
from datetime import datetime
import os, asyncio, requests
from dotenv import load_dotenv

load_dotenv()  # Carga variables de entorno desde .env en local

app = FastAPI()

HEADERS = {"Content-Type": "application/json"}
webhook_active = False

# Define el modelo de datos para la suscripción
class Subscription(BaseModel):
    username: str
    monthly_fee: float
    start_date: datetime

@app.get("/")
def read_root():
    return {"mensaje": "Servidor activo con configuración desde entorno"}

# Endpoint para iniciar el envío del webhook
# Recibe un cuerpo de tipo Subscription y lo envía periódicamente
@app.post("/start")
async def start_webhook(body: Subscription, background_tasks: BackgroundTasks):
    global webhook_active
    webhook_active = True
    background_tasks.add_task(send_webhook, body)
    return {"mensaje": "Envío iniciado"}

# Endpoint para detener el envío del webhook
# Cambia el estado de webhook_active a False para detener el envío
@app.post("/stop")
def stop_webhook():
    global webhook_active
    webhook_active = False
    return {"mensaje": "Envío detenido"}

# Función que envía el webhook periódicamente
# Utiliza la variable de entorno WEBHOOK_URL para definir el destino del webhook
async def send_webhook(body: Subscription):
    contador = 1
    url = os.getenv("WEBHOOK_URL")
    sleep_time = int(os.getenv("TIME_SLEEP", 5))

    if not url:
        print("No se encontró la variable WEBHOOK_URL.")
        return

    while webhook_active:
        payload = {
            "mensaje": "Hola desde Python",
            "usuario": body.username,
            "timestamp": datetime.now().isoformat(),
            "numero_envio": contador,
            "cuota_mensual": body.monthly_fee,
            "fecha_inicio": body.start_date.isoformat()
        }

        try:
            response = requests.post(url, json=payload, headers=HEADERS)
            print(f"Envío #{contador} - Estado: {response.status_code}")
        except Exception as e:
            print(f"Error al enviar webhook: {e}")

        contador += 1
        await asyncio.sleep(sleep_time)