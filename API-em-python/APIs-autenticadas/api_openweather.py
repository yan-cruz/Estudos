import os
from pprint import pprint
import requests
import dotenv

def fazer_request(url, params=None):
    response = requests.get(url, params=params)

    try:
        response.raise_for_status()
    except requests.HTTPError as e:
        print(f'Erro no request: {e}')
        resultado = None
    else:
        resultado = response.json()
    return resultado

dotenv.load_dotenv()
token = os.environ['OPENWEATHER_TOKEN']

url = 'https://api.openweathermap.org/data/2.5/weather'
params = {
    'appid': token,
    'q': 'Divinópolis',
    'units': 'metric'
}

def main():
    dados = fazer_request(url, params)
    pprint(dados)

if __name__ == '__main__':
    main()