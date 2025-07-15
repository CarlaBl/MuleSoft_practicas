import requests
import time
import random

def run_tests(endpoint: str, interval: int = 30):
    print(f"Simulando registros cada {interval}s hacia {endpoint}")
    try:
        while True:
            user_data = {
                "username": random.choice(["carla_dev", "admin_test", "tester_api", "usuario_demo"]),
                "password": str(random.randint(100000, 999999))
            }
            try:
                response = requests.post(endpoint, json=user_data)
                print(f"Enviado: {user_data['username']} ({response.status_code})")
            except Exception as e:
                print("Error al enviar:", e)

            time.sleep(interval)
    except KeyboardInterrupt:
        print("Simulación detenida manualmente.")