import requests
from main import headers
from main import battles

def coletar_dados_api():
    url = ''
    try:
        resposta = requests.get(url, headers=headers)  
        resposta.raise_for_status()
        return resposta.json().get('items', []) 
    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar a API: {e}")
        return []

def salvar_dados_mongo(dados):
    if dados:
        battles.insert_many(dados)  
        print(f"{len(dados)} batalhas inseridas com sucesso!")
    else:
        print("Nenhum dado para salvar.")

dados = coletar_dados_api()
salvar_dados_mongo(dados)