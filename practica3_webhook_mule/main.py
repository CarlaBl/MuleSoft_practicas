from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
from datetime import datetime
from dotenv import load_dotenv
import os, asyncio, requests
import xml.etree.ElementTree as ET

load_dotenv()  # Carga variables de entorno desde .env en local

app = FastAPI()
webhook_active = False
# HEADERS = {"Content-Type": "application/json"} = archivo JSON
# Cambiamos a XML para el contenido del webhook
HEADERS = {"Content-Type": "application/xml"}


# Define el modelo de datos para el cuerpo del webhook
class Employee(BaseModel):
    first_name: str
    last_name: str
    email: str
    hire_date: datetime
    job_id: str
    salary: float


# Endpoint para verificar que el servidor está activo
@app.get("/")
def read_root():
    return {"mensaje": "Servidor activo con configuración desde entorno"}

# Endpoint para iniciar el envío del webhook
# Recibe un cuerpo de tipo Subscription y lo envía periódicamente
@app.post("/start")
async def start_webhook(body: Employee, background_tasks: BackgroundTasks):
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


#Construir XML dinámico con contador como ID
def build_xml_payload(body, id_actual):
    # Construir el XML con los datos del empleado
    root = ET.Element("employee")
    ET.SubElement(root, "employee_id").text = str(id_actual)
    ET.SubElement(root, "first_name").text = body.first_name
    ET.SubElement(root, "last_name").text = body.last_name
    ET.SubElement(root, "email").text = body.email
    ET.SubElement(root, "hire_date").text = body.hire_date.isoformat()
    ET.SubElement(root, "job_id").text = body.job_id
    ET.SubElement(root, "salary").text = str(body.salary)
    return ET.tostring(root, encoding="utf-8")


# Función que envía el webhook periódicamente
# Utiliza la variable de entorno WEBHOOK_URL para definir el destino del webhook
async def send_webhook(body: Employee):
    
    url = os.getenv("WEBHOOK_URL")
    sleep_time = int(os.getenv("TIME_SLEEP", 5)) # Tiempo de espera entre envíos, por defecto 5 segundos
    id_inicial = int(os.getenv("ID_INICIAL", 1000)) # Valor por defecto si no se define en .env
    contador = id_inicial

    if not url:
        print("No se encontró la variable WEBHOOK_URL.")
        return

    while webhook_active:
        xml_data = build_xml_payload(body, contador)
        ''' archivo JSON de ejemplo
            payload = {
                "first_name": "Carla",
                "last_name": "Blacio",
                "email": "carla.blacio@example.com",
                "hire_date": "2025-07-21T15:36:00",
                "job_id": "IT_PROG",
                "salary": 60000
                }
        '''
        try:
            response = requests.post(url, data=xml_data, headers=HEADERS)
            print(f"Envío xml #{contador} - Estado: {response.status_code}")
        except Exception as e:
            print(f"Error al enviar webhook: {e}")

        contador += 1
        await asyncio.sleep(sleep_time)