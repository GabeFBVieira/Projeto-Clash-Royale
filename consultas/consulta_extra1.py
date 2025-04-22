from main import battles

def executar():
    pipeline = [
        {"$unwind": "$team"},
        {"$unwind": "$team.cards"},
        {"$group": {
            "_id": "$team.cards.name",
            "count": {"$sum": 1}
        }},
        {
            "$group": {
                "_id": None,
                "total": {"$sum": "$count"},
                "cards": {"$push": {"card": "$_id", "count": "$count"}}
            }
        },
        {"$unwind": "$cards"},
        {
            "$project": {
                "_id": 0,
                "card": "$cards.card",
                "count": "$cards.count",
                "percentual": {
                    "$round": [
                        {"$multiply": [
                            {"$divide": ["$cards.count", "$total"]},
                            100
                        ]},
                        2
                    ]
                }
            }
        },
        {"$sort": {"percentual": -1}},
        {"$limit": 20}
    ]

    return list(battles.aggregate(pipeline))
