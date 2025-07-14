import requests
import json
import time
import datetime

url = "https://webhook.site/97fe5127-0ca1-4981-8c18-77256d8c9c03"
headers = {
    "Content-Type": "application/json"
}

print(" Iniciando envío de webhooks cada 2 segundos...")
print(" Presiona Ctrl+C para detener")
print("=" * 50)

contador = 1

try:
    while True:
        # Crear payload con timestamp y contador
        payload = {
            "mensaje": "Hola desde Python xd",
            "usuario": "Emiliano",
            "tecnologia": "Webhook + JSON",
            "timestamp": datetime.datetime.now().isoformat(),
            "numero_envio": contador
        }
        
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        
        # Mostrar información del envío
        tiempo_actual = datetime.datetime.now().strftime('%H:%M:%S')
        print(f" Envío #{contador} - Estado: {response.status_code} - Hora: {tiempo_actual}")
        
        contador += 1
        time.sleep(1)  # Esperar 2 segundos
        
except KeyboardInterrupt:
    print(f"\n Detenido por el usuario")
    print(f" Total de envíos realizados: {contador - 1}")