from main import battles
from datetime import datetime

# porcentagem para mais de 10% de vitórias
from dotenv import load_dotenv
import os
from pymongo import MongoClient

# 1) Carrega variáveis de ambiente e conecta
load_dotenv()
client = MongoClient(os.getenv("MONGOKEY"))
db = client["bd_clashroyale"]
battles = db["battles"]

# 2) Filtro de vitórias (battleTime como STRING ISO) de 1 a 19 de abril
match_wins = {
    "battleTime": {
        "$gte": "20250401T000000.000Z",
        "$lte": "20250419T235959.999Z"
    },
    "$expr": {
        "$gt": [
            {"$arrayElemAt": ["$team.crowns", 0]},
            {"$arrayElemAt": ["$opponent.crowns", 0]} 
        ]
    }
}

# 3) Conta o total de vitórias no período
total_wins = battles.count_documents(match_wins)
print(f"Total de vitórias no período: {total_wins}\n")

if total_wins == 0:
    print("Não há vitórias registradas nesse intervalo.")
    exit()

# 4) Pipeline para extrair combos com ≥1 carta de elixirCost ≥ 1
pipeline = [
    {"$match": match_wins},
    {"$addFields": {
        "filtered": {
            "$filter": {
                "input": "$team.cards",
                "as": "c",
                "cond": {"$gte": ["$$c.elixirCost", 1]}
            }
        }
    }},
    {"$match": {"$expr": {"$gte": [{"$size": "$filtered"}, 1]}}},
    {"$project": {
        "combo": {
            "$map": {
                "input": "$filtered",
                "as": "c",
                "in": "$$c.name"
            }
        }
    }},
    # Ordena o combo para agrupamento consistente (MongoDB >=5.2)
    {"$addFields": {
        "combo": {"$sortArray": {"input": "$combo", "sortBy": 1}}
    }},
    {"$group": {
        "_id": "$combo",
        "count": {"$sum": 1}
    }},
    {"$project": {
        "_id": 0,
        "combo": "$_id",
        "count": 1
    }}
]

# 5) Executa o aggregation e imprime apenas combos com >10% de vitórias
results = list(battles.aggregate(pipeline))

print("Combos com >10% de vitórias (≥1 carta de elixir ≥1):")
found = False
for doc in results:
    combo = doc["combo"]
    # Achata quaisquer listas internas
    flat = []
    for elt in combo:
        if isinstance(elt, list):
            flat.extend(elt)
        else:
            flat.append(elt)
    combo_str = ", ".join(flat)
    pct = doc["count"] / total_wins * 100
    if pct > 10:
        print(f" • [{combo_str}] → {doc['count']}/{total_wins} partidas ({pct:.2f}%)")
        found = True

if not found:
    print("Nenhum combo atingiu mais de 10% das vitórias.")
