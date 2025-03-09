import os
from pprint import pprint
from requests.auth import HTTPBasicAuth
import streamlit as st
import requests
import dotenv

dotenv.load_dotenv()

def autenticar():
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
        token = None
    else:
        token = response.json()['access_token']
        return token

def busca_artista(nome_artista, headers):
    url = 'https://api.spotify.com/v1/search'
    params = {
        'q': nome_artista,
        'type': 'artist'
    }

    response = requests.get(url=url, headers=headers, params=params)
    try:
        melhor_resposta = response.json()['artists']['items'][0]
    except IndexError:
        melhor_resposta = None
    return melhor_resposta

def busca_top_musicas(id_artist, headers):
    url = f'https://api.spotify.com/v1/artists/{id_artist}/top-tracks'

    response = requests.get(url=url, headers=headers)
    return response.json()['tracks']

def converter_ms_para_min_seg(ms):
    segundos = ms / 1000
    minutos = int(segundos // 60)
    segundos = int(segundos % 60)
    return f'{minutos:02}:{segundos:02}'

def main():
    st.title('Web API - Top Tracks de um Artista')
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
    for i, (musicas) in enumerate(top_musicas, start=1):
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

if __name__ == '__main__':
    main()