from main import players

def executar():
    pipeline = [
        {
            "$project": {
                "name": 1,
                "winRate": {
                    "$cond": [
                        { "$gt": ["$battleCount", 0] },
                        { "$multiply": [{ "$divide": ["$wins", "$battleCount"] }, 100] },
                        0
                    ]
                }
            }
        },
        { "$sort": { "winRate": -1 } }
    ]

    return list(players.aggregate(pipeline))
