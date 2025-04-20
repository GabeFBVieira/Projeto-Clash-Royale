import requests
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import headers, players

def coletar_dados_api(urls):
    dados = []

    for url in urls:
        try:
            resposta = requests.get(url, headers=headers)
            resposta.raise_for_status()
            dados.append(resposta.json())
        except requests.exceptions.RequestException as e:
            print(f"Erro ao acessar a API para URL {url}: {e}")

    return dados

def salvar_dados_mongo(dados):
    if dados:
        players.insert_many(dados)
        print(f"{len(dados)} registros inseridos com sucesso!")
    else:
        print("Nenhum dado para salvar.")

urls = [
    'https://api.clashroyale.com/v1/players/%239QQ2J2ULL',
    'https://api.clashroyale.com/v1/players/%23U8RYGC8GU',
    'https://api.clashroyale.com/v1/players/%23R2PLLVCY8',
    'https://api.clashroyale.com/v1/players/%23GUPVGVQQV',
    'https://api.clashroyale.com/v1/players/%232U0J8RCYJ'
]

dados = coletar_dados_api(urls)
salvar_dados_mongo(dados)
