import requests
import os
import dotenv
from pprint import pprint
import pandas as pd

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
'''since_date = input("Digite a data de início (YYYY-MM-DD): ")
until_date = input("Digite a data de término (YYYY-MM-DD): ")'''

since_date = "2025-04-01"
until_date = "2025-04-05"

# Validar se as datas foram fornecidas
if not since_date or not until_date:
    print("Erro: As datas de início e término são obrigatórias.")
    exit()

# Parâmetros da requisição
fields = (
    f"adaccounts.limit(100){{"
    f"name,"
    f"insights.time_range({{'since':'{since_date}','until':'{until_date}'}}){{"
    f"spend,purchase_roas,actions,action_values"
    f"}}"
    f"}}"
)

params = {
    "fields": fields,
    "access_token": token
}

# Fazer a requisição GET
response = fazer_request(url, params=params)

# Lista para armazenar todos os clientes processados
clientes = []

for account in response.get('adaccounts', {}).get('data', []):
    cliente = {}
    cliente['nome'] = account.get('name', 'Desconhecido')
    
    # Verificar se há insights disponíveis
    insights_data = account.get('insights', {}).get('data', [])
    if insights_data:
        # Investimento
        insights = insights_data[0]
        cliente['investimento'] = float(insights.get('spend', 0.0))
        
        # ROAS
        purchase_roas = insights.get('purchase_roas', [])
        cliente['roas'] = float(purchase_roas[0]['value']) if purchase_roas else 0.0

        # Compras
        actions = insights.get('actions', [])
        cliente['compras'] = 0

        for action in actions:
            if action.get('action_type') == 'purchase':
                cliente['compras'] = int(float(action.get('value', 0)))
                break

        # Valor de conversão
        action_values = insights.get('action_values', [])
        cliente['retorno'] = 0

        for action in action_values:
            if action.get('action_type') == 'purchase':
                cliente['retorno'] = float(action.get('value', 0))
                break

    else:
        # Caso não haja insights, definir valores padrão
        cliente['investimento'] = 0.0
        cliente['roas'] = 0.0
        cliente['compras'] = 0
        cliente['adicoes_carrinho'] = 0
    
    # Adiciona na lista
    clientes.append(cliente)

# Agora você tem uma lista de dicionários limpa e fácil de filtrar:
for c in clientes:
    print(c)
