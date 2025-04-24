from main import battles
from datetime import datetime,time

def executar(cartas, data_inicio:datetime, data_fim:datetime):
  
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
                "team.cards.name": { "$all": cartas },
                "battleTimeDate": {
                    "$gte": datetime.combine(data_inicio, time.min),
                    "$lte": datetime.combine(data_fim, time.max)
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
