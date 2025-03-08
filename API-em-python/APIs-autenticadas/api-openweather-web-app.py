import os
from pprint import pprint
import streamlit as st
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

def pegar_tempo(local):
    dotenv.load_dotenv()
    token = os.environ['OPENWEATHER_TOKEN']

    url = 'https://api.openweathermap.org/data/2.5/weather'
    params = {
        'appid': token,
        'q': local,
        'units': 'metric',
        'lang': 'pt_br',
    }
    dados_tempo = fazer_request(url=url, params=params)
    return dados_tempo

def main():
    st.title('Web API - Dados do Clima')
    st.write('Dados via OpenWeather (fonte: https://openweathermap.org/current)')

    local = st.text_input('Digite o nome da cidade:')
    if not local:
        st.stop()

    dados_tempo = pegar_tempo(local=local)
    if not dados_tempo:
        st.warning(f'Nenhum dado encontrado para {local}.')
        st.stop()

    clima_atual = dados_tempo['weather'][0]['description']
    temperatura = dados_tempo['main']['temp']
    sensacao_termica = dados_tempo['main']['feels_like']
    umidade = dados_tempo['main']['humidity']
    nuvens = dados_tempo['clouds']['all']
    icone = dados_tempo['weather'][0]['icon']

    icone_url =  f'https://openweathermap.org/img/wn/{icone}@2x.png'

    # st.metric(label='Clima Atual', value=clima_atual.title())

    st.markdown('<span style="font-size: 14px; margin: 0;">Clima Atual</span>', unsafe_allow_html=True)
    st.markdown(
        f"""
        <div style="display: flex; align-items: center; margin: 0;">
            <span style="font-size: 2em; margin: 0;">{clima_atual.title()}</span>
            <img src="{icone_url}" width="50" style="margin-left: 10px;">
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown('<style>p { margin: 0; }</style>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.metric(label='Temperatura', value=f'{temperatura}°C')
        st.metric(label='Umidade', value=f'{umidade}%')

    with col2:
        st.metric(label='Sensação Térmica', value=f'{sensacao_termica}°C')
        st.metric(label='Cobertura das Nuvens', value=f'{nuvens}%')

    pprint(dados_tempo)

if __name__ == '__main__':
    main()