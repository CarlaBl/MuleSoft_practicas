import requests
import json
import time
import datetime

url = "https://webhook.site/cb3d1df6-5b34-4478-814f-1b838635be0f"
headers = {
    "Content-Type": "application/json"
}

print(" Iniciando envío de webhooks cada 5 segundos...")
print(" Presiona Ctrl+C para detener")
print("=" * 30)

contador = 1

try:
    while True:
        # Crear payload con timestamp y contador
        payload = {
            "mensaje": "Hola desde Python",
            "usuario": "Carla",
            "tecnologia": "Webhook + JSON",
            "timestamp": datetime.datetime.now().isoformat(),
            "numero_envio": contador
        }
        
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        
        # Mostrar información del envío
        tiempo_actual = datetime.datetime.now().strftime('%H:%M:%S')
        print(f" Envío #{contador} - Estado: {response.status_code} - Hora: {tiempo_actual}")
        
        contador += 1
        time.sleep(5)  # Esperar 5 segundos
        
except KeyboardInterrupt:
    print(f"\n Detenido por el usuario")
    print(f" Total de envíos realizados: {contador - 1}")