import os
import requests
from pprint import pprint
import streamlit as st
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

def pegar_nome_decada(nome):
    url = f'https://servicodados.ibge.gov.br/api/v2/censos/nomes/{nome}'
    dados_decadas = fazer_request(url=url)
    if not dados_decadas:
        return {}
    dict_decadas = {}
    for dados in dados_decadas[0]['res']:
        decada = dados['periodo']
        quantidade = dados['frequencia']
        dict_decadas[decada] = quantidade
    return dict_decadas



def main():
    st.title('Web API - Nomes')
    st.write('Dados via IBGE (fonte: https://servicodados.ibge.gov.br/api/docs/nomes?versao=2)')

    nome = st.text_input('Digite um nome:')
    if not nome:
        st.stop()

    dict_decadas = pegar_nome_decada(nome)
    if not dict_decadas:
        st.warning(f'Nenhum registro encontrado para {nome}.')
        st.stop()

    df = pd.DataFrame.from_dict(dict_decadas, orient='index')

    col1, col2 = st.columns([0.3, 0.7])

    with col1:
        st.write('Frequência por década:')
        st.dataframe(df)

    with col2:
        st.write('Evolução com o tempo:')
        st.line_chart(df)

if __name__ == '__main__':
    main()