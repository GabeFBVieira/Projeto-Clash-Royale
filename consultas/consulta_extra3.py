from main import players

pipeline = [
    
    { "$project": {
        "name":    1,
        "winRate": {
            "$cond": [
                { "$gt": ["$battleCount", 0] },
                { "$divide": ["$wins", "$battleCount"] },
                0
            ]
        }
    }},
 
    { "$sort": { "winRate": -1 } }

]

all_ranked = list(players.aggregate(pipeline))

print("Ranking de aproveitamento de todos os jogadores:")
for idx, p in enumerate(all_ranked, start=1):
    print(f"{idx:>2}. {p['name']:<20} — {p['winRate']*100:6.2f}%")
