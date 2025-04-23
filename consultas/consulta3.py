from main import battles
from datetime import datetime

def executar(cartas, data_inicio, data_fim):
    # Converter date para datetime (caso necessário)
    if isinstance(data_inicio, datetime):
        data_inicio = data_inicio
    else:
        data_inicio = datetime.combine(data_inicio, datetime.min.time())

    if isinstance(data_fim, datetime):
        data_fim = data_fim
    else:
        data_fim = datetime.combine(data_fim, datetime.max.time())

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
                "team.0.cards.name": { "$all": cartas },
                "battleTimeDate": {
                    "$gte": data_inicio,
                    "$lte": data_fim
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

    return list(battles.aggregate(pipeline))
