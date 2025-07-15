from datetime import datetime
import requests
import json
import asyncio
import os


from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
from typing import List
from tester_module import run_tests

app = FastAPI()

# Archivo de guardado de datos
DATA_FILE = "db.json"
HEADERS = {"Content-Type": "application/json"}

# Estructura de datos de un registro
class Register(BaseModel):
    username: str
    password: str
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()

"""
    API (Aqui nosotros vamos a ver los datos que tenemos y trabajaremos con ellos)
"""
@app.get("/")
def read_root():
    return {"mensaje": "Servidor de Webhook activo"}

# Iniciar simulación de registros
@app.get("/start-simulation")
def start_simulation(background_tasks: BackgroundTasks, intervalo: int = 30):
    # URL dónde tenemos desplegada la API
    webhook_url = "https://mulesoft-practicas.onrender.com/webhook/new-register"
    background_tasks.add_task(run_tests, webhook_url, intervalo)
    return {"mensaje": f"Simulación iniciada cada {intervalo} segundos."}


@app.get("/api/users/")
def get_users():
    if not os.path.exists(DATA_FILE):
        return {"mensaje": "Archivo no encontrado"}

    try:
        with open(DATA_FILE, "r") as f:
            contenido = f.read().strip()
            if not contenido:
                return {"mensaje": "Archivo vacío"}
            data = json.loads(contenido)
            return data
    except json.JSONDecodeError:
        return {"mensaje": "El archivo contiene datos inválidos"}

"""
    WEBHOOK (Aqui nos va a avisar otro servidor cuando se registren en el)
"""
@app.post("/webhook/new-register")
def new_register(body: Register, background_tasks: BackgroundTasks):
    background_tasks.add_task(newRegister, body)
    return {"mensaje": "Webhook iniciado en segundo plano."}

# Guardar el nuevo registro en db.json
def newRegister(body: Register):
    nuevo = body.dict()

    # Lee si existe el archivo de db.json si no lo crea
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            contenido = f.read().strip()
            if contenido:
                try:
                    data = json.loads(contenido)
                except json.JSONDecodeError:
                    data = []
            else:
                data = []
    else:
        data = []

    # Agregar nuevo registro
    data.append(nuevo)

    # Guardar en archivo
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4, default=str)
