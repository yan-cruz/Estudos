import os
import requests
from pprint import pprint

os.system('cls')

def pegar_ids_estados():
    url = 'https://servicodados.ibge.gov.br/api/v1/localidades/estados'
    params = {
        'view': 'nivelado'
    }
    dados_estados = fazer_request(url=url, params=params)
    dict_estado = {}
    for dados in dados_estados:
        id_estado = dados['UF-id']
        nome_estado = dados['UF-nome']
        dict_estado[id_estado] = nome_estado
    return dict_estado

def pegar_frequencia_nome_estados(nome):
    url = f'https://servicodados.ibge.gov.br/api/v2/censos/nomes/{nome}'
    params = {
        'groupBy': 'UF'
    }
    dados_frequencias = fazer_request(url=url, params=params)
    dict_frequencias = {}
    for dados in dados_frequencias:
        id_estado = int(dados['localidade'])
        frequencia = dados['res'][0]['proporcao']
        dict_frequencias[id_estado] = frequencia
    return dict_frequencias

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

def main():
    nome =  input('Digite um nome: ')
    dict_estados = pegar_ids_estados()
    dict_frequencias = pegar_frequencia_nome_estados(nome)
    estados_ordenados = sorted(dict_estados.items(), key=lambda x: dict_frequencias[x[0]], reverse=True)
    print(f'Frequência do nome {nome} nos Estado (por 100.000 habitantes):\n')
    for i, (id_estado, nome_estado) in enumerate(estados_ordenados, start=1):
        frequencia_estado = dict_frequencias[id_estado]
        print(f'{i}° -  {nome_estado}: {frequencia_estado}')

if __name__ == '__main__':
    main()