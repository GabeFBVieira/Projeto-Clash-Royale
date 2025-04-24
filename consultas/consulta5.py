from datetime import datetime
from main import battles

def executar(data_inicio, data_fim, porcentagem_minima):
   
    start_str = data_inicio.strftime("%Y%m%dT%H%M%S.000Z")
    end_str = data_fim.strftime("%Y%m%dT%H%M%S.000Z")

    print("Data início:", start_str)
    print("Data fim:", end_str)

    
    match_wins = {
        "battleTime": {
            "$gte": start_str,
            "$lte": end_str
        },
        "$expr": {
            "$gt": [
                {"$arrayElemAt": ["$team.crowns", 0]},
                {"$arrayElemAt": ["$opponent.crowns", 0]}
            ]
        }
    }

    total_wins = battles.count_documents(match_wins)
    print(f"Total de vitórias no período: {total_wins}")

    if total_wins == 0:
        print("Nenhuma vitória encontrada.")
        return []


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


    results = list(battles.aggregate(pipeline))

    print("Resultados da agregação:", results)


    combos_filtrados = []
    for doc in results:
        combo = doc["combo"]
        flat = []
        for elt in combo:
            if isinstance(elt, list):
                flat.extend(elt)
            else:
                flat.append(elt)
        pct = doc["count"] / total_wins * 100
        if pct >= porcentagem_minima:
            combos_filtrados.append({
                "combo": flat,
                "count": doc["count"],
                "percent": round(pct, 2)
            })

    return combos_filtrados

data_inicio = datetime(2025, 4, 1)
data_fim = datetime(2025, 4, 19)
porcentagem_minima = 2  

resultados = executar(data_inicio, data_fim, porcentagem_minima)
print("Resultados finais:", resultados)
