import requests
import pymongo
from pymongo import MongoClient
client = MongoClient()

client = pymongo.MongoClient('Mongo link connection Here')

db = client['bd_clashroyale']

cards = db['cards']

headers = {
'Content-type':'application/json',
'Authorization':'Bearer token here'
}

def coletar_dados_api():
    url = 'https://api.clashroyale.com/v1/cards'
    try:
        resposta = requests.get(url, headers=headers)  
        resposta.raise_for_status()
        return resposta.json().get('items', []) 
    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar a API: {e}")
        return []

def salvar_dados_mongo(dados):
    if dados:
        cards.insert_many(dados)  
        print(f"{len(dados)} cartas inseridas com sucesso!")
    else:
        print("Nenhum dado para salvar.")

dados = coletar_dados_api()
salvar_dados_mongo(dados)


