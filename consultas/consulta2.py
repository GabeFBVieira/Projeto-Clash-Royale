import streamlit as st
from datetime import datetime, time
from main import battles

def executar(percentual: float, data_inicio: datetime, data_fim: datetime):
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
                    "$gte": datetime.combine(data_inicio, time.min),
                    "$lte": datetime.combine(data_fim, time.max)
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
                "totalVitorias": { "$sum": { "$cond": ["$vitoria", 1, 0] } }
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
        { "$match": { "taxaVitorias": { "$gte": percentual } } },
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
    
    brutos = list(battles.aggregate(pipeline))
    resultados = []

    for r in brutos:
        cartas = r.get("deck", [])
        nomes = []

        for carta in cartas:
            if isinstance(carta, dict) and "name" in carta:
                nomes.append(carta["name"])
            elif isinstance(carta, list):
                nomes.extend([item["name"] for item in carta if isinstance(item, dict) and "name" in item])

        resultados.append({
            "deck": ", ".join(nomes) if nomes else "Desconhecido",
            "totalPartidas": r.get("totalPartidas", 0),
            "totalVitorias": r.get("totalVitorias", 0),
            "taxaVitorias": r.get("taxaVitorias", 0.0)
        })

    return resultados