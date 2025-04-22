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


    dados_tabela = []
    for jogador in resultados:
        for carta in jogador["cards"]:
            dados_tabela.append({
                "Jogador": jogador["player"],
                "Carta": carta["card"],
                "Usos": carta["count"]
            })

    return dados_tabela
