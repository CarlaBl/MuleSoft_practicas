import requests
import json
import time
from datetime import datetime

# URL de Webhook.site
WEBHOOK_URL = "https://webhook.site/db676ba8-962e-4e5b-86e2-9f7da048c4fe"

headers = {
    "Content-Type": "application/json"
}

print("Enviando 5 mensajes cada 5 segundos...\n")

for i in range(1, 6):
    payload = {
        "mensaje": "Prueba independiente",
        "numero_envio": i,
        "timestamp": datetime.now().isoformat(),
        "usuario": "carla",
        "tecnologia": "Python puro + requests"
    }

    response = requests.post(WEBHOOK_URL, data=json.dumps(payload), headers=headers)

    print(f"✅ Envío #{i} - Status: {response.status_code} - Hora: {datetime.now().strftime('%H:%M:%S')}")
    time.sleep(5)

print("\n Prueba terminada.")