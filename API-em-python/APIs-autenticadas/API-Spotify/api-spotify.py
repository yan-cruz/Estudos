import os
from pprint import pprint
from requests.auth import HTTPBasicAuth
import requests
import dotenv

dotenv.load_dotenv()
client_id = os.environ['CLIENT_ID']
client_secret = os.environ['CLIENT_SECRET']

auth = HTTPBasicAuth(username=client_id, password=client_secret)

url = 'https://accounts.spotify.com/api/token'
body = {
    'grant_type': 'client_credentials'
}

response = requests.post(url=url, data=body, auth=auth)

try:
    response.raise_for_status()
except requests.HTTPError as e:
    print(f'Erro no request: {e}')
    resultado = None
else:
    resultado = response.json()

id_artist = '2PLF4pjm6A5eztTVbt9ou4'
url = f'https://api.spotify.com/v1/artists/{id_artist}'
headers = {
    'Authorization': f'Bearer {resultado['access_token']}'
}

response = requests.get(url=url, headers=headers)

pprint(response.json())