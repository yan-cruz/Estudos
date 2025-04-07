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
token = os.environ['ACCESS_TOKEN']

# URL da API
url = "https://graph.facebook.com/v22.0/me"

# Solicitar as datas ao usuário
since_date = input("Digite a data de início (YYYY-MM-DD): ")
until_date = input("Digite a data de término (YYYY-MM-DD): ")

# Validar se as datas foram fornecidas
if not since_date or not until_date:
    print("Erro: As datas de início e término são obrigatórias.")
    exit()

# Parâmetros da requisição
fields = (
    f"adaccounts.limit(100){{"
    f"name,"
    f"insights.time_range({{'since':'{since_date}','until':'{until_date}'}}){{"
    f"spend,purchase_roas"
    f"}}"
    f"}}"
)

params = {
    "fields": fields,
    "access_token": token
}

# Fazer a requisição GET
response = fazer_request(url, params=params)

# Verificar o resultado
if response:
    pprint(response)