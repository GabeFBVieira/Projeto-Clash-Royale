import requests
import pymongo
from pymongo import MongoClient
client = MongoClient()

client = pymongo.MongoClient('mongodb+srv://padeiro:pao@cluster-gabe.eakkboc.mongodb.net/')

db = client['bd_clashroyale']

cards = db['cards']

headers = {
'Content-type':'application/json',
'Authorization':'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjBiYzQ3NmM3LTEyZjItNDYxZC1iOWE1LTY1Y2E1YTA5MWYwMCIsImlhdCI6MTc0NDMzMzcwMiwic3ViIjoiZGV2ZWxvcGVyL2M1YWZlMjc3LTRkMjktOWE2My04NmU5LWVkNGZmNmQzZTMxNSIsInNjb3BlcyI6WyJyb3lhbGUiXSwibGltaXRzIjpbeyJ0aWVyIjoiZGV2ZWxvcGVyL3NpbHZlciIsInR5cGUiOiJ0aHJvdHRsaW5nIn0seyJjaWRycyI6WyIxODEuMjIyLjEyMC4yMzUiXSwidHlwZSI6ImNsaWVudCJ9XX0.Vcq4przZkV6VCmKrJ54N93XAt4XrsbFUX-X7pbI7pn39GS1Ai-1A0a62tGl1RoEeGHenkAzPjgKS4PncxGJuuQ'
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


