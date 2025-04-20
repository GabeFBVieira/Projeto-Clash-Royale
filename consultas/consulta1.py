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
    { "$unwind": "$team" },
    { "$unwind": "$team.cards" },
    {
        "$match": {
            "team.cards.name": "Musketeer",
            "battleTimeDate": {
                "$gte": datetime(2025, 1, 1, 0, 0, 0),
                "$lte": datetime(2025, 12, 31, 23, 59, 59)
            }
        }
    },
    {
        "$group": {
            "_id": "$team.cards.name",
            "total": { "$sum": 1 },
            "vitorias": {
                "$sum": {
                    "$cond": [
                        {
                            "$gt": [
                                "$team.crowns",
                                { "$max": "$opponent.crowns" }
                            ]
                        },
                        1,
                        0
                    ]
                }
            }
        }
    },
    {
        "$project": {
            "_id": 0,
            "carta": "$_id",
            "total": 1,
            "vitorias": 1,
            "taxa_vitorias": {
                "$multiply": [
                    { "$divide": ["$vitorias", "$total"] },
                    100
                ]
            }
        }
    },
    { "$sort": { "taxa_vitorias": -1 } }
]

resultados = list(battles.aggregate(pipeline))

for r in resultados:
    print(f"Carta: {r['carta']}")
    print(f"Total: {r['total']}")
    print(f"Vitórias: {r['vitorias']}")
    print(f"Taxa de Vitórias: {r['taxa_vitorias']:.2f}%")
    print("-" * 30)
