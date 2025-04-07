import os
from pprint import pprint
import streamlit as st
import requests
import dotenv
from requests.auth import HTTPBasicAuth

dotenv.load_dotenv()

# Funções do primeiro código (Spotify)
def autenticar():
    '''Usada para autenticar o cliente na API do Spotify'''
    client_id = os.environ['CLIENT_ID']
    client_secret = os.environ['CLIENT_SECRET']

    auth = HTTPBasicAuth(username=client_id, password=client_secret)

    url = 'https://accounts.spotify.com/api/token'
    body = {
        'grant_type': 'client_credentials'
    }

    response = requests.post(url=url, data=body, auth=auth, timeout=10)

    try:
        response.raise_for_status()
    except requests.HTTPError as e:
        print(f'Erro no request: {e}')
        token = None
    else:
        token = response.json()['access_token']
        return token

def busca_artista(nome_artista, headers):
    '''Realiza a busca do artista pesquisado, retornando o primeiro resultado'''
    url = 'https://api.spotify.com/v1/search'
    params = {
        'q': nome_artista,
        'type': 'artist'
    }

    response = requests.get(url=url, headers=headers, params=params, timeout=10)
    try:
        melhor_resposta = response.json()['artists']['items'][0]
    except IndexError:
        melhor_resposta = None
    return melhor_resposta

def busca_top_musicas(id_artist, headers):
    '''Busca as músicas mais ouvidas do artista escolhido'''
    url = f'https://api.spotify.com/v1/artists/{id_artist}/top-tracks'

    response = requests.get(url=url, headers=headers, timeout=10)
    return response.json()['tracks']

def converter_ms_para_min_seg(ms):
    '''Converte a duração da música, útil para unir posteriormente ao nome'''
    segundos = ms / 1000
    minutos = int(segundos // 60)
    segundos = int(segundos % 60)
    return f'{minutos:02}:{segundos:02}'

# Funções do segundo código (Clima)
def fazer_request(url, params=None):
    '''Retorna os dados do local escolhido'''
    response = requests.get(url, params=params, timeout=10)

    try:
        response.raise_for_status()
    except requests.HTTPError as e:
        print(f'Erro no request: {e}')
        resultado = None
    else:
        resultado = response.json()
    return resultado

def pegar_tempo(local):
    '''Retorna os dados do clima do local'''
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
    '''Main da aplicação'''
    st.title('Hub de APIs: Spotify & Clima')

    opcao = st.radio("Escolha o serviço", ('Buscar Top Músicas de Artista', 'Consultar Clima'))

    if opcao == 'Buscar Top Músicas de Artista':
        st.write('Dados via Spotify (fonte: https://developer.spotify.com/documentation/web-api)')
        
        nome = st.text_input('Busque um artista:')
        if not nome:
            st.stop()

        token = autenticar()
        headers = {
            'Authorization': f'Bearer {token}'
        }

        artista = busca_artista(nome, headers)
        if not artista:
            st.warning(f'Nenhum dado encontrado para {nome}')
            st.stop()

        id_artist = artista['id']
        nome_artista = artista['name']
        url_capa = artista['images'][0]['url']

        st.markdown('<span style="font-size: 17px; margin: 0; margin-bottom: 20px; ">As mais ouvidas de:</span>', unsafe_allow_html=True)

        st.markdown(
            f"""
            <div style="display: flex; align-items: center; margin: 0; margin-bottom: 30px;">
                <img src="{url_capa}" width="120" style="border-radius: 50%; margin-right: 30px;">
                <span style="font-size: 2em; margin: 0; display: inline-block; vertical-align: middle;">{nome_artista.title()}</span>
            </div>
            """,
            unsafe_allow_html=True
        )

        top_musicas = busca_top_musicas(id_artist=id_artist, headers=headers)
        for i, musicas in enumerate(top_musicas, start=1):
            duracao_musica = musicas['duration_ms']
            nome_musica = f"{musicas['name']} ({converter_ms_para_min_seg(duracao_musica)})"
            link_musica = musicas['external_urls']['spotify']
            st.markdown(
                f"""
                <style>
                    a {{
                        color: inherit !important; 
                    }}
                </style>
                {i}° -  <a href="{link_musica}">{nome_musica}</a>
                """,
                unsafe_allow_html=True
            )

    elif opcao == 'Consultar Clima':
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
