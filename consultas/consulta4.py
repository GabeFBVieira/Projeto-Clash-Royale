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

from main import battles

def executar(carta, desvantagem_minima):
    fator_desvantagem = 1 - (desvantagem_minima / 100)

    pipeline = [
        {
            '$match': {
                '$or': [
                    { 'team.cards.name': carta },
                    { 'opponent.cards.name': carta }
                ]
            }
        },
        {
            '$addFields': {
                'teamTrophies': { '$arrayElemAt': ['$team.startingTrophies', 0] },
                'opponentTrophies': { '$arrayElemAt': ['$opponent.startingTrophies', 0] }
            }
        },
        {
            '$addFields': {
                'teamWon': { '$gt': [ { '$arrayElemAt': ['$team.crowns', 0] }, { '$arrayElemAt': ['$opponent.crowns', 0] } ] },
                'opponentWon': { '$gt': [ { '$arrayElemAt': ['$opponent.crowns', 0] }, { '$arrayElemAt': ['$team.crowns', 0] } ] }
            }
        },
        {
            '$match': {
                '$or': [
                    {
                        'teamWon': True,
                        '$expr': {
                            '$lt': [
                                '$teamTrophies',
                                { '$multiply': ['$opponentTrophies', fator_desvantagem] }
                            ]
                        }
                    },
                    {
                        'opponentWon': True,
                        '$expr': {
                            '$lt': [
                                '$opponentTrophies',
                                { '$multiply': ['$teamTrophies', fator_desvantagem] }
                            ]
                        }
                    }
                ]
            }
        },
        {
            '$match': {
                '$or': [
                    {
                        'teamWon': True,
                        '$expr': {
                            '$or': [
                                { '$eq': ['$opponent.princessTowersHitPoints', None] },
                                { '$lt': [ { '$size': '$opponent.princessTowersHitPoints' }, 2 ] }
                            ]
                        }
                    },
                    {
                        'opponentWon': True,
                        '$expr': {
                            '$or': [
                                { '$eq': ['$team.princessTowersHitPoints', None] },
                                { '$lt': [ { '$size': '$team.princessTowersHitPoints' }, 2 ] }
                            ]
                        }
                    }
                ]
            }
        },
        {
            '$count': 'quantidadeVitorias'
        }
    ]

    resultado = list(battles.aggregate(pipeline))

    if resultado:
        return resultado[0]['quantidadeVitorias']
    else:
        return 0
