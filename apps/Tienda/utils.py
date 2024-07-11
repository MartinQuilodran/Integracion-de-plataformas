import requests
from requests.exceptions import RequestException
import json


def enviar_solicitud_transbank(url, data):
    headers = {
        'Content-Type': 'application/json',
        'Tbk-Api-Key-Id': '597055555532',  # Reemplaza con tu API Key ID
        'Tbk-Api-Key-Secret': '579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C'  # Reemplaza con tu API Key Secret
    }

    try:
        # Debug: Imprimir datos de la solicitud
        print(f"Enviando datos a Transbank: {json.dumps(data, indent=2)}")
        
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()  # Esto lanzará un error si el código de estado HTTP es 4xx o 5xx
        return response.json()
    except RequestException as e:
        print(f"Error en la solicitud a Transbank: {e}")
        return {"error": str(e), "status_code": response.status_code if response else "No Response"}

