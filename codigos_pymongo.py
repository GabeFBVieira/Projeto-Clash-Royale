# -------------------- consulta 1 --------------------
# from datetime import datetime
# from main import battles

# pipeline = [
#     {
#         "$addFields": {
#             "battleTimeDate": {
#                 "$dateFromString": {
#                     "dateString": "$battleTime",
#                     "format": "%Y%m%dT%H%M%S.%LZ"
#                 }
#             }
#         }
#     },
#     { "$unwind": "$team" },
#     { "$unwind": "$team.cards" },
#     {
#         "$match": {
#             "team.cards.name": "Musketeer",
#             "battleTimeDate": {
#                 "$gte": datetime(2025, 1, 1, 0, 0, 0),
#                 "$lte": datetime(2025, 12, 31, 23, 59, 59)
#             }
#         }
#     },
#     {
#         "$group": {
#             "_id": "$team.cards.name",
#             "total": { "$sum": 1 },
#             "vitorias": {
#                 "$sum": {
#                     "$cond": [
#                         {
#                             "$gt": [
#                                 "$team.crowns",
#                                 { "$max": "$opponent.crowns" }
#                             ]
#                         },
#                         1,
#                         0
#                     ]
#                 }
#             }
#         }
#     },
#     {
#         "$project": {
#             "_id": 0,
#             "carta": "$_id",
#             "total": 1,
#             "vitorias": 1,
#             "taxa_vitorias": {
#                 "$multiply": [
#                     { "$divide": ["$vitorias", "$total"] },
#                     100
#                 ]
#             }
#         }
#     },
#     { "$sort": { "taxa_vitorias": -1 } }
# ]

# resultados = list(battles.aggregate(pipeline))

# for r in resultados:
#     print(f"Carta: {r['carta']}")
#     print(f"Total: {r['total']}")
#     print(f"Vitórias: {r['vitorias']}")
#     print(f"Taxa de Vitórias: {r['taxa_vitorias']:.2f}%")
#     print("-" * 30)

# -------------------- consulta 2 --------------------
# from datetime import datetime
# from main import battles

# pipeline = [
#     {
#         "$addFields": {
#             "battleTimeDate": {
#                 "$dateFromString": {
#                     "dateString": "$battleTime",
#                     "format": "%Y%m%dT%H%M%S.%LZ"
#                 }
#             }
#         }
#     },
#     {
#         "$match": {
#             "battleTimeDate": {
#                 "$gte": datetime(2025, 1, 1, 0, 0, 0),
#                 "$lte": datetime(2025, 12, 31, 23, 59, 59)
#             }
#         }
#     },
#     {
#         "$addFields": {
#             "vitoria": {
#                 "$gt": [
#                     { "$arrayElemAt": ["$team.crowns", 0] },
#                     { "$max": "$opponent.crowns" }
#                 ]
#             }
#         }
#     },
#     {
#         "$group": {
#             "_id": "$team.cards",
#             "totalPartidas": { "$sum": 1 },
#             "totalVitorias": {
#                 "$sum": {
#                     "$cond": ["$vitoria", 1, 0]
#                 }
#             }
#         }
#     },
#     {
#         "$addFields": {
#             "taxaVitorias": {
#                 "$multiply": [
#                     { "$divide": ["$totalVitorias", "$totalPartidas"] },
#                     100
#                 ]
#             }
#         }
#     },
#     {
#         "$match": {
#             "taxaVitorias": { "$gte": 60 }
#         }
#     },
#     {
#         "$project": {
#             "_id": 0,
#             "deck": "$_id",
#             "totalPartidas": 1,
#             "totalVitorias": 1,
#             "taxaVitorias": { "$round": ["$taxaVitorias", 2] }
#         }
#     },
#     { "$sort": { "taxaVitorias": -1 } }
# ]

# resultados = list(battles.aggregate(pipeline))


# for r in resultados:
   
#     deck_nomes = []
#     for cards in r['deck']:  
#         for card in cards[:8]:  
            
#             deck_nomes.append(card.get('name', 'Desconhecido'))


#     deck_str = ", ".join(deck_nomes[:8])

#     print(f"Deck: {deck_str}")
#     print(f"Total de Partidas: {r['totalPartidas']}")
#     print(f"Total de Vitórias: {r['totalVitorias']}")
#     print(f"Taxa de Vitórias: {r['taxaVitorias']}%")
#     print("-" * 30)

# -------------------- consulta 3 --------------------
# from main import battles
# from datetime import datetime

#     pipeline = [
#         {
#             "$addFields": {
#                 "battleTimeDate": {
#                     "$dateFromString": {
#                         "dateString": "$battleTime",
#                         "format": "%Y%m%dT%H%M%S.%LZ"
#                     }
#                 }
#             }
#         },
#         {
#             "$match": {
#                 "team.0.cards.name": { "$all": cartas },
#                 "battleTimeDate": {
#                     "$gte": data_inicio,
#                     "$lte": data_fim
#                 }
#             }
#         },
#         {
#             "$addFields": {
#                 "derrota": {
#                     "$lt": [
#                         { "$arrayElemAt": ["$team.crowns", 0] },
#                         { "$arrayElemAt": ["$opponent.crowns", 0] }
#                     ]
#                 }
#             }
#         },
#         {
#             "$group": {
#                 "_id": None,
#                 "totalDerrotas": { "$sum": { "$cond": ["$derrota", 1, 0] } },
#                 "totalPartidas": { "$sum": 1 }
#             }
#         },
#         {
#             "$project": {
#                 "_id": 0,
#                 "totalPartidas": 1,
#                 "totalDerrotas": 1,
#                 "taxaDerrotas": {
#                     "$round": [
#                         {
#                             "$multiply": [
#                                 { "$divide": ["$totalDerrotas", "$totalPartidas"] },
#                                 100
#                             ]
#                         },
#                         2
#                     ]
#                 }
#             }
#         }
#     ]

#     return list(battles.aggregate(pipeline))

# -------------------- consulta 4 --------------------
# from main import battles


# pipeline = [
#     {
#         '$match': {
#             '$or': [
#                 { 'team.cards.name': 'Arrows' },
#                 { 'opponent.cards.name': 'Arrows' }
#             ]
#         }
#     },
   
#     {
#         '$addFields': {
#             'teamTrophies': { '$arrayElemAt': ['$team.startingTrophies', 0] },
#             'opponentTrophies': { '$arrayElemAt': ['$opponent.startingTrophies', 0] }
#         }
#     },
  
#     {
#         '$addFields': {
#             'teamWon': { '$gt': [ { '$arrayElemAt': ['$team.crowns', 0] }, { '$arrayElemAt': ['$opponent.crowns', 0] } ] },
#             'opponentWon': { '$gt': [ { '$arrayElemAt': ['$opponent.crowns', 0] }, { '$arrayElemAt': ['$team.crowns', 0] } ] }
#         }
#     },
 
#     {
#         '$match': {
#             '$or': [
#                 {
#                     'teamWon': True,
#                     '$expr': {
#                         '$lt': [
#                             '$teamTrophies',
#                             { '$multiply': ['$opponentTrophies', 0.9] }
#                         ]
#                     }
#                 },
#                 {
#                     'opponentWon': True,
#                     '$expr': {
#                         '$lt': [
#                             '$opponentTrophies',
#                             { '$multiply': ['$teamTrophies', 0.9] }
#                         ]
#                     }
#                 }
#             ]
#         }
#     },
    
#     {
#         '$match': {
#             '$or': [
#                 {
#                     'teamWon': True,
#                     '$expr': {
#                         '$or': [
#                             { '$eq': ['$opponent.princessTowersHitPoints', None] },
#                             { '$lt': [ { '$size': '$opponent.princessTowersHitPoints' }, 2 ] }
#                         ]
#                     }
#                 },
#                 {
#                     'opponentWon': True,
#                     '$expr': {
#                         '$or': [
#                             { '$eq': ['$team.princessTowersHitPoints', None] },
#                             { '$lt': [ { '$size': '$team.princessTowersHitPoints' }, 2 ] }
#                         ]
#                     }
#                 }
#             ]
#         }
#     },
  
#     {
#         '$count': 'quantidadeVitorias'
#     }
# ]

# resultado = list(battles.aggregate(pipeline))

# if resultado:
#     print(f'Quantidade de vitórias com Arrows, 10% menos troféus e oponente destruiu 2 torres: {resultado[0]["quantidadeVitorias"]}')
# else:
#     print('Não foi encontrada nenhuma vitória com Arrows, 10% menos troféus e oponente com 2 torres destruídas.')

# -------------------- consulta 5 --------------------

# -------------------- consulta extra1 --------------------
# from main import battles

# pipeline = [
#         {"$unwind": "$team"},
#         {"$unwind": "$team.cards"},
#         {"$group": {
#             "_id": "$team.cards.name",
#             "count": {"$sum": 1}
#         }},
#         {
#             "$group": {
#                 "_id": None,
#                 "total": {"$sum": "$count"},
#                 "cards": {"$push": {"card": "$_id", "count": "$count"}}
#             }
#         },
#         {"$unwind": "$cards"},
#         {
#             "$project": {
#                 "_id": 0,
#                 "card": "$cards.card",
#                 "count": "$cards.count",
#                 "percentual": {
#                     "$round": [
#                         {"$multiply": [
#                             {"$divide": ["$cards.count", "$total"]},
#                             100
#                         ]},
#                         2
#                     ]
#                 }
#             }
#         },
#         {"$sort": {"percentual": -1}},
#         {"$limit": 20}
#     ]

#     return list(battles.aggregate(pipeline))

# -------------------- consulta extra2 --------------------
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

# -------------------- consulta extra3 --------------------
# from main import players

# pipeline = [
#         {
#             "$project": {
#                 "name": 1,
#                 "winRate": {
#                     "$cond": [
#                         { "$gt": ["$battleCount", 0] },
#                         { "$multiply": [{ "$divide": ["$wins", "$battleCount"] }, 100] },
#                         0
#                     ]
#                 }
#             }
#         },
#         { "$sort": { "winRate": -1 } }
#     ]

#     return list(players.aggregate(pipeline))