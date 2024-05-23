import requests

def enviar_solicitud_transbank(url, data):
    headers = {
        'Tbk-Api-Key-Id': '597055555532',
        'Tbk-Api-Key-Secret': '579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C',
        'Content-Type': 'application/json',
    }
    response = requests.post(url, json=data, headers=headers)
    return response.json()
