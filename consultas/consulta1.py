from datetime import datetime
from main import battles

def executar(carta: str, data_inicio: datetime, data_fim: datetime):
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
                "team.cards.name": carta,
                "battleTimeDate": {
                    "$gte": datetime.combine(data_inicio, datetime.min.time()),
                    "$lte": datetime.combine(data_fim, datetime.max.time())
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
                            { "$gt": ["$team.crowns", { "$max": "$opponent.crowns" }] },
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
    return resultados
