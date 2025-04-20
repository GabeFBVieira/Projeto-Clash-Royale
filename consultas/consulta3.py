from main import battles
from datetime import datetime

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
            "team.0.cards.name": { "$all": ["Musketeer", "Skeletons", "Miner"] },
            "battleTimeDate": {
                "$gte": datetime(2025, 4, 1, 0, 0, 0),
                "$lte": datetime(2025, 4, 20, 23, 59, 59)
            }
        }
    },
    {
        "$addFields": {
            "derrota": {
                "$lt": [
                    { "$arrayElemAt": ["$team.crowns", 0] },
                    { "$arrayElemAt": ["$opponent.crowns", 0] }
                ]
            }
        }
    },
    {
        "$group": {
            "_id": None,
            "totalDerrotas": { "$sum": { "$cond": ["$derrota", 1, 0] } },
            "totalPartidas": { "$sum": 1 }
        }
    },
    {
        "$project": {
            "_id": 0,
            "totalPartidas": 1,
            "totalDerrotas": 1,
            "taxaDerrotas": {
                "$round": [
                    {
                        "$multiply": [
                            { "$divide": ["$totalDerrotas", "$totalPartidas"] },
                            100
                        ]
                    },
                    2
                ]
            }
        }
    }
]


resultados = list(battles.aggregate(pipeline))


for r in resultados:
    print(f"Total de Partidas: {r['totalPartidas']}")
    print(f"Total de Derrotas: {r['totalDerrotas']}")
    print(f"Taxa de Derrotas: {r['taxaDerrotas']}%")
    print("-" * 30)
