from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGOKEY = os.getenv('MONGOKEY')
API_KEY = os.getenv('API_KEY')

client = MongoClient(MONGOKEY)
db = client['bd_clashroyale']

headers = {
    'Content-type': 'application/json',
    'Authorization': f'Bearer {API_KEY}' 
}

battles  = db['battles']
players  = db['players']