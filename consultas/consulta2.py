from datetime import datetime
from main import battles

pipeline = [
    {
        "$addFields": {
            "battleTimeDate": {
                "$dateFromString": {
                    "dateString": "$battleTime",
                    "format": "%Y%m%dT%H%M%S.%LZ"
                }
            }
        }
    },
    {
        "$match": {
            "battleTimeDate": {
                "$gte": datetime(2025, 1, 1, 0, 0, 0),
                "$lte": datetime(2025, 12, 31, 23, 59, 59)
            }
        }
    },
    {
        "$addFields": {
            "vitoria": {
                "$gt": [
                    { "$arrayElemAt": ["$team.crowns", 0] },
                    { "$max": "$opponent.crowns" }
                ]
            }
        }
    },
    {
        "$group": {
            "_id": "$team.cards",
            "totalPartidas": { "$sum": 1 },
            "totalVitorias": {
                "$sum": {
                    "$cond": ["$vitoria", 1, 0]
                }
            }
        }
    },
    {
        "$addFields": {
            "taxaVitorias": {
                "$multiply": [
                    { "$divide": ["$totalVitorias", "$totalPartidas"] },
                    100
                ]
            }
        }
    },
    {
        "$match": {
            "taxaVitorias": { "$gte": 60 }
        }
    },
    {
        "$project": {
            "_id": 0,
            "deck": "$_id",
            "totalPartidas": 1,
            "totalVitorias": 1,
            "taxaVitorias": { "$round": ["$taxaVitorias", 2] }
        }
    },
    { "$sort": { "taxaVitorias": -1 } }
]

resultados = list(battles.aggregate(pipeline))


for r in resultados:
   
    deck_nomes = []
    for cards in r['deck']:  
        for card in cards[:8]:  
            
            deck_nomes.append(card.get('name', 'Desconhecido'))


    deck_str = ", ".join(deck_nomes[:8])

    print(f"Deck: {deck_str}")
    print(f"Total de Partidas: {r['totalPartidas']}")
    print(f"Total de Vitórias: {r['totalVitorias']}")
    print(f"Taxa de Vitórias: {r['taxaVitorias']}%")
    print("-" * 30)

