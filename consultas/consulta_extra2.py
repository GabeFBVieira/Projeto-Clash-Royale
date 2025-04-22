# from main import battles

# # Lista dos players que você indicou
# valid_players = ["ALONE", "DuffStunts", "WL ツ Dam’s ✨", "Polaris", "Rage"]

# pipeline = [
#     { "$unwind": "$team" },
#     { "$match": {
#         "team.name":            { "$in": valid_players },
#         "team.startingTrophies": { "$gte": 8000 }    
#     }},
#     { "$unwind": "$team.cards" },
#     { "$group": {
#         "_id": {
#             "player": "$team.name",
#             "card":   "$team.cards.name"
#         },
#         "count": { "$sum": 1 }
#     }},
#     { "$sort": {
#         "_id.player": 1,
#         "count":      -1
#     }},
#     { "$group": {
#         "_id":   "$_id.player",
#         "cards": {
#             "$push": {
#                 "card":  "$_id.card",
#                 "count": "$count"
#             }
#         }
#     }},
#     { "$project": {
#         "_id":    0,
#         "player": "$_id",
#         "cards":  1
#     }}
# ]

# result = list(battles.aggregate(pipeline))

# for doc in result:
#     print(f"\n {doc['player']} — cartas usadas (maior pra menor):")
#     for c in doc["cards"]:
#         print(f"   • {c['card']} — {c['count']}x")

from main import battles

# Lista dos jogadores analisados
valid_players = ["ALONE", "DuffStunts", "WL ツ Dam’s ✨", "Polaris", "Rage"]

def executar():
    pipeline = [
        { "$unwind": "$team" },
        { "$match": {
            "team.name": { "$in": valid_players },
            "team.startingTrophies": { "$gte": 8000 }
        }},
        { "$unwind": "$team.cards" },
        { "$group": {
            "_id": {
                "player": "$team.name",
                "card": "$team.cards.name"
            },
            "count": { "$sum": 1 }
        }},
        { "$sort": {
            "_id.player": 1,
            "count": -1
        }},
        { "$group": {
            "_id": "$_id.player",
            "cards": {
                "$push": {
                    "card": "$_id.card",
                    "count": "$count"
                }
            }
        }},
        { "$project": {
            "_id": 0,
            "player": "$_id",
            "cards": 1
        }}
    ]

    resultados = list(battles.aggregate(pipeline))

    # Reformata os dados para exibição em tabela
    dados_tabela = []
    for jogador in resultados:
        for carta in jogador["cards"]:
            dados_tabela.append({
                "Jogador": jogador["player"],
                "Carta": carta["card"],
                "Usos": carta["count"]
            })

    return dados_tabela
