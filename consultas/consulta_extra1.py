from main import battles


pipeline = [
    {"$unwind": "$team"},                   
    {"$unwind": "$team.cards"},             
    {"$group": {                              
        "_id": "$team.cards.name",
        "count": {"$sum": 1}                
    }},
    {"$sort": {"count": -1}},               
    {"$limit": 20},                          
    {"$project": {"_id": 0, "card": "$_id", "count": 1}}  
]


top_cards = list(battles.aggregate(pipeline))
print("Top 20 cartas mais utilizadas nos decks do time (aggregate simples):\n")
for i, doc in enumerate(top_cards, start=1):
    print(f"{i:2}. {doc['card']} — {doc['count']} vezes")
