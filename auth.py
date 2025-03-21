import requests

CLIENT_ID = "7634906846936710"
CLIENT_SECRET = "YNfo5NSqHsqNpa2HRWD39O54KJw2pAnS"

def obtener_access_token():
    url = "https://api.mercadolibre.com/oauth/token"
    data = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }

    response = requests.post(url, data=data)

    if response.status_code == 200:
        access_token = response.json().get("access_token")
        print("Nuevo Access Token:", access_token)
        return access_token
    else:
        print("❌ Error al obtener el Access Token:", response.status_code, response.text)
        return None  # Retorna None si falla
