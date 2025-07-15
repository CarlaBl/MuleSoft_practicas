import requests
import time
import random
import argparse

# Argumentos para personalizar
parser = argparse.ArgumentParser(description="Simulador de registros al webhook.")
parser.add_argument("--interval", type=int, default=15, help="Tiempo entre envíos (en segundos)")
parser.add_argument("--endpoint", type=str, default="http://localhost:8000/webhook/new-register", help="URL del webhook")
args = parser.parse_args()

INTERVAL_SECONDS = args.interval
WEBHOOK_ENDPOINT = args.endpoint

# Generador de datos falsos
def generate_fake_user():
    nombres = ["carla_dev", "admin_test", "usuario_demo", "tester_api", "mod_invitado"]
    return {
        "username": random.choice(nombres),
        "password": str(random.randint(100000, 999999))
    }

# Ciclo principal
def run_tests():
    print("Iniciando simulación de registros al webhook...")
    print(f"Endpoint: {WEBHOOK_ENDPOINT}")
    print(f"Intervalo configurado: {INTERVAL_SECONDS} segundos\n")
    print("Presiona Ctrl+C para detener la simulación.\n")

    try:
        while True:
            user_data = generate_fake_user()
            try:
                response = requests.post(WEBHOOK_ENDPOINT, json=user_data)
                status = response.status_code
                print(f"Enviado: {user_data['username']} ({status})")
            except Exception as e:
                print("Error al enviar:", e)

            print(f"Esperando {INTERVAL_SECONDS} segundos...\n")
            time.sleep(INTERVAL_SECONDS)

    except KeyboardInterrupt:
        print("\n Simulación detenida por el usuario.")

if __name__ == "__main__":
    run_tests()