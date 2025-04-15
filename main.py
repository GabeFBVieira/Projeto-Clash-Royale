import requests
import pymongo
from dotenv import load_dotenv
import os
from pymongo import MongoClient

# Carregar as variáveis de ambiente do arquivo .env
load_dotenv()

# Acessar as variáveis de ambiente
API_KEY = os.getenv('API_KEY')
MONGOKEY = os.getenv('MONGOKEY')

# Conectar ao MongoDB usando a chave de conexão (MONGOKEY)
client = MongoClient(MONGOKEY)

# Conectar ao banco de dados específico
db = client['bd_clashroyale']

# Acessar as coleções
players = db['players']
battles = db['battles']

# Definir os cabeçalhos para a API com o valor real da variável API_KEY
headers = {
    'Content-type': 'application/json',
    'Authorization': f'Bearer {API_KEY}'  # Corrigido: API_KEY no cabeçalho de autorização
}

# URL do jogador
url = "https://api.clashroyale.com/v1/players/%239QQ2J2ULL"

# Fazer a requisição para a API
response = requests.get(url, headers=headers)

# Verificar o status da resposta
if response.status_code == 200:
    data = response.json()
    print(data)
else:
    print(f"Erro ao acessar a API: {response.status_code} - {response.text}")
