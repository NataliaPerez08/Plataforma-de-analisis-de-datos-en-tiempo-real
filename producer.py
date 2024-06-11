import requests
from kafka import KafkaProducer
import json
import time

import os
# Reemplaza 'YOUR_API_TOKEN' con tu token de acceso de INEGI
api_token = os.getenv('INEGI_API_TOKEN')
base_url = 'https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/INDICATOR/6200060874/es/0700/false/BISE/2.0/{token}?type=json'
url = base_url.format(token=api_token)

producer = KafkaProducer(bootstrap_servers='kafka:9092',
                         value_serializer=lambda x: json.dumps(x).encode('utf-8'))

def fetch_data():
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        producer.send('inegi_poblacion', value=data)
        print("Datos enviados a Kafka:", data)
    else:
        print(f"Error {response.status_code}: {response.text}")

if __name__ == '__main__':
    while True:
        fetch_data()
        time.sleep(3600)  # Esperar 1 hora antes de la siguiente consulta
