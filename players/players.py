import requests
import sys
import os

# Adiciona o diretório raiz (Projeto-Clash-Royale) ao sys.path
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

# Lista de URLs dos jogadores
urls = [
    'https://api.clashroyale.com/v1/players/%239QQ2J2ULL',
    'https://api.clashroyale.com/v1/players/%2388P2JYY8R',
    'https://api.clashroyale.com/v1/players/%2382Y88QUVQ'
]

dados = coletar_dados_api(urls)
salvar_dados_mongo(dados)
