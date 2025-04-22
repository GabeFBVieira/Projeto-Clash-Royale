# from main import battles
# from datetime import datetime

# porcentagem para mais de 10% de vitórias
# from dotenv import load_dotenv
# import os
# from pymongo import MongoClient

# # 1) Carrega variáveis de ambiente e conecta
# load_dotenv()
# client = MongoClient(os.getenv("MONGOKEY"))
# db = client["bd_clashroyale"]
# battles = db["battles"]

# # 2) Filtro de vitórias (battleTime como STRING ISO) de 1 a 19 de abril
# match_wins = {
#     "battleTime": {
#         "$gte": "20250401T000000.000Z",
#         "$lte": "20251231T235959.999Z"
#     },
#     "$expr": {
#         "$gt": [
#             {"$arrayElemAt": ["$team.crowns", 0]},
#             {"$arrayElemAt": ["$opponent.crowns", 0]} 
#         ]
#     }
# }

# # 3) Conta o total de vitórias no período
# total_wins = battles.count_documents(match_wins)
# print(f"Total de vitórias no período: {total_wins}\n")

# if total_wins == 0:
#     print("Não há vitórias registradas nesse intervalo.")
#     exit()

# # 4) Pipeline para extrair combos com ≥1 carta de elixirCost ≥ 1
# pipeline = [
#     {"$match": match_wins},
#     {"$addFields": {
#         "filtered": {
#             "$filter": {
#                 "input": "$team.cards",
#                 "as": "c",
#                 "cond": {"$gte": ["$$c.elixirCost", 1]}
#             }
#         }
#     }},
#     {"$match": {"$expr": {"$gte": [{"$size": "$filtered"}, 1]}}},
#     {"$project": {
#         "combo": {
#             "$map": {
#                 "input": "$filtered",
#                 "as": "c",
#                 "in": "$$c.name"
#             }
#         }
#     }},
#     # Ordena o combo para agrupamento consistente (MongoDB >=5.2)
#     {"$addFields": {
#         "combo": {"$sortArray": {"input": "$combo", "sortBy": 1}}
#     }},
#     {"$group": {
#         "_id": "$combo",
#         "count": {"$sum": 1}
#     }},
#     {"$project": {
#         "_id": 0,
#         "combo": "$_id",
#         "count": 1
#     }}
# ]

# # 5) Executa o aggregation e imprime apenas combos com >10% de vitórias
# results = list(battles.aggregate(pipeline))

# print("Combos com >10% de vitórias (≥1 carta de elixir ≥1):")
# found = False
# for doc in results:
#     combo = doc["combo"]
#     # Achata quaisquer listas internas
#     flat = []
#     for elt in combo:
#         if isinstance(elt, list):
#             flat.extend(elt)
#         else:
#             flat.append(elt)
#     combo_str = ", ".join(flat)
#     pct = doc["count"] / total_wins * 100
#     if pct > 10:
#         print(f" • [{combo_str}] → {doc['count']}/{total_wins} partidas ({pct:.2f}%)")
#         found = True

# if not found:
#     print("Nenhum combo atingiu mais de 10% das vitórias.")


#  funcionou no streamlit mas não a consulta -  consultas/consulta5.py
# from pymongo import MongoClient
# from dotenv import load_dotenv
# import os

# load_dotenv()
# client = MongoClient(os.getenv("MONGOKEY"))
# db = client["bd_clashroyale"]
# battles = db["battles"]

# def executar(data_inicio, data_fim):
#     start_str = data_inicio.strftime("%Y%m%dT000000.000Z")
#     end_str = data_fim.strftime("%Y%m%dT235959.999Z")

#     match_wins = {
#         "battleTime": {
#             "$gte": start_str,
#             "$lte": end_str
#         },
#         "$expr": {
#             "$gt": [
#                 {"$arrayElemAt": ["$team.crowns", 0]},
#                 {"$arrayElemAt": ["$opponent.crowns", 0]}
#             ]
#         }
#     }

#     total_wins = battles.count_documents(match_wins)

#     if total_wins == 0:
#         return []

#     pipeline = [
#         {"$match": match_wins},
#         {"$addFields": {
#             "filtered": {
#                 "$filter": {
#                     "input": "$team.cards",
#                     "as": "c",
#                     "cond": {"$gte": ["$$c.elixirCost", 1]}
#                 }
#             }
#         }},
#         {"$match": {"$expr": {"$gte": [{"$size": "$filtered"}, 1]}}},
#         {"$project": {
#             "combo": {
#                 "$map": {
#                     "input": "$filtered",
#                     "as": "c",
#                     "in": "$$c.name"
#                 }
#             }
#         }},
#         {"$addFields": {
#             "combo": {"$sortArray": {"input": "$combo", "sortBy": 1}}
#         }},
#         {"$group": {
#             "_id": "$combo",
#             "count": {"$sum": 1}
#         }},
#         {"$project": {
#             "_id": 0,
#             "combo": "$_id",
#             "count": 1
#         }}
#     ]

#     results = list(battles.aggregate(pipeline))

#     print("Vitórias no período:", total_wins)

#     combos_filtrados = []
#     for doc in results:
#         combo = doc["combo"]
#         flat = []
#         for elt in combo:
#             if isinstance(elt, list):
#                 flat.extend(elt)
#             else:
#                 flat.append(elt)
#         pct = doc["count"] / total_wins * 100
#         if pct > 2:
#             combos_filtrados.append({
#                 "combo": flat,
#                 "count": doc["count"],
#                 "percent": round(pct, 2)
#             })

#     return combos_filtrados

# --- retornou nada no terminal e no streamlit deu vazio 
# from pymongo import MongoClient
# from dotenv import load_dotenv
# import os
# from datetime import datetime

# load_dotenv()
# client = MongoClient(os.getenv("MONGOKEY"))
# db = client["bd_clashroyale"]
# battles = db["battles"]

# def executar(data_inicio, data_fim):
#     # Convertendo para o formato ISO 8601
#     start_str = data_inicio.isoformat()  # Exemplo: "2025-04-01T00:00:00"
#     end_str = data_fim.isoformat()  # Exemplo: "2025-04-19T23:59:59"

#     match_wins = {
#         "battleTime": {
#             "$gte": start_str,
#             "$lte": end_str
#         },
#         "$expr": {
#             "$gt": [
#                 {"$arrayElemAt": ["$team.crowns", 0]},
#                 {"$arrayElemAt": ["$opponent.crowns", 0]}
#             ]
#         }
#     }

#     total_wins = battles.count_documents(match_wins)

#     if total_wins == 0:
#         return []

#     pipeline = [
#         {"$match": match_wins},
#         {"$addFields": {
#             "filtered": {
#                 "$filter": {
#                     "input": "$team.cards",
#                     "as": "c",
#                     "cond": {"$gte": ["$$c.elixirCost", 1]}
#                 }
#             }
#         }},
#         {"$match": {"$expr": {"$gte": [{"$size": "$filtered"}, 1]}}},
#         {"$project": {
#             "combo": {
#                 "$map": {
#                     "input": "$filtered",
#                     "as": "c",
#                     "in": "$$c.name"
#                 }
#             }
#         }},
#         {"$addFields": {
#             "combo": {"$sortArray": {"input": "$combo", "sortBy": 1}}
#         }},
#         {"$group": {
#             "_id": "$combo",
#             "count": {"$sum": 1}
#         }},
#         {"$project": {
#             "_id": 0,
#             "combo": "$_id",
#             "count": 1
#         }}
#     ]

#     results = list(battles.aggregate(pipeline))
    
#     print("Vitórias no período:", total_wins)

#     combos_filtrados = []
#     for doc in results:
#         combo = doc["combo"]
#         flat = []
#         for elt in combo:
#             if isinstance(elt, list):
#                 flat.extend(elt)
#             else:
#                 flat.append(elt)
#         pct = doc["count"] / total_wins * 100
#         if pct > 2:
#             combos_filtrados.append({
#                 "combo": flat,
#                 "count": doc["count"],
#                 "percent": round(pct, 2)
#             })

#     return combos_filtrados

# from pymongo import MongoClient
# from dotenv import load_dotenv
# import os
# from datetime import datetime

# load_dotenv()
# client = MongoClient(os.getenv("MONGOKEY"))
# db = client["bd_clashroyale"]
# battles = db["battles"]

# def executar(data_inicio, data_fim):
#     # Convertendo para o formato ISO 8601
#     start_str = data_inicio.isoformat()  # Exemplo: "2025-04-01T00:00:00"
#     end_str = data_fim.isoformat()  # Exemplo: "2025-04-19T23:59:59"

#     match_wins = {
#         "battleTime": {
#             "$gte": start_str,
#             "$lte": end_str
#         },
#         "$expr": {
#             "$gt": [
#                 {"$arrayElemAt": ["$team.crowns", 0]},
#                 {"$arrayElemAt": ["$opponent.crowns", 0]}
#             ]
#         }
#     }

#     total_wins = battles.count_documents(match_wins)

#     print(f"Total de vitórias encontradas no período: {total_wins}")

#     if total_wins == 0:
#         return []

#     # Debugging: Verificar os documentos correspondentes
#     print("Documentos encontrados (match_wins):")
#     for battle in battles.find(match_wins).limit(5):  # Limita para verificar alguns resultados
#         print(battle)

#     pipeline = [
#         {"$match": match_wins},
#         {"$addFields": {
#             "filtered": {
#                 "$filter": {
#                     "input": "$team.cards",
#                     "as": "c",
#                     "cond": {"$gte": ["$$c.elixirCost", 1]}
#                 }
#             }
#         }},
#         {"$match": {"$expr": {"$gte": [{"$size": "$filtered"}, 1]}}},
#         {"$project": {
#             "combo": {
#                 "$map": {
#                     "input": "$filtered",
#                     "as": "c",
#                     "in": "$$c.name"
#                 }
#             }
#         }},
#         {"$addFields": {
#             "combo": {"$sortArray": {"input": "$combo", "sortBy": 1}}
#         }},
#         {"$group": {
#             "_id": "$combo",
#             "count": {"$sum": 1}
#         }},
#         {"$project": {
#             "_id": 0,
#             "combo": "$_id",
#             "count": 1
#         }}
#     ]

#     results = list(battles.aggregate(pipeline))

#     # Depuração: Verificar os resultados intermediários
#     print("Combos encontrados (pipeline):")
#     for result in results[:5]:  # Limita para verificar alguns resultados
#         print(result)

#     combos_filtrados = []
#     for doc in results:
#         combo = doc["combo"]
#         flat = []
#         for elt in combo:
#             if isinstance(elt, list):
#                 flat.extend(elt)
#             else:
#                 flat.append(elt)
#         pct = doc["count"] / total_wins * 100
#         if pct > 2:
#             combos_filtrados.append({
#                 "combo": flat,
#                 "count": doc["count"],
#                 "percent": round(pct, 2)
#             })

#     return combos_filtrados


# ------ 
# from pymongo import MongoClient
# from dotenv import load_dotenv
# import os
# from datetime import datetime

# load_dotenv()
# client = MongoClient(os.getenv("MONGOKEY"))
# db = client["bd_clashroyale"]
# battles = db["battles"]

# def executar(data_inicio, data_fim):
#     # Convertendo para o formato "YYYY-MM-DDTHH:MM:SS"
#     start_str = data_inicio.strftime("%Y-%m-%dT%H:%M:%S")  # Exemplo: "2025-04-01T00:00:00"
#     end_str = data_fim.strftime("%Y-%m-%dT%H:%M:%S")  # Exemplo: "2025-04-19T23:59:59"

#     # Filtro de vitórias baseado no tempo
#     match_wins = {
#         "battleTime": {
#             "$gte": start_str,
#             "$lte": end_str
#         },
#         "$expr": {
#             "$gt": [
#                 {"$arrayElemAt": ["$team.crowns", 0]},
#                 {"$arrayElemAt": ["$opponent.crowns", 0]}
#             ]
#         }
#     }

#     # Depuração: Verificar as datas no banco
#     print(f"Procurando vitórias entre: {start_str} e {end_str}")

#     total_wins = battles.count_documents(match_wins)

#     print(f"Total de vitórias encontradas no período: {total_wins}")

#     if total_wins == 0:
#         print("Nenhuma vitória encontrada. Verifique o filtro de datas e vitórias.")
#         return []

#     # Debugging: Verificar alguns documentos correspondentes ao filtro
#     print("Documentos encontrados (match_wins):")
#     for battle in battles.find(match_wins).limit(5):  # Limita para verificar alguns resultados
#         print(battle)

#     pipeline = [
#         {"$match": match_wins},
#         {"$addFields": {
#             "filtered": {
#                 "$filter": {
#                     "input": "$team.cards",
#                     "as": "c",
#                     "cond": {"$gte": ["$$c.elixirCost", 1]}
#                 }
#             }
#         }},
#         {"$match": {"$expr": {"$gte": [{"$size": "$filtered"}, 1]}}},
#         {"$project": {
#             "combo": {
#                 "$map": {
#                     "input": "$filtered",
#                     "as": "c",
#                     "in": "$$c.name"
#                 }
#             }
#         }},
#         {"$addFields": {
#             "combo": {"$sortArray": {"input": "$combo", "sortBy": 1}}
#         }},
#         {"$group": {
#             "_id": "$combo",
#             "count": {"$sum": 1}
#         }},
#         {"$project": {
#             "_id": 0,
#             "combo": "$_id",
#             "count": 1
#         }}
#     ]

#     results = list(battles.aggregate(pipeline))

#     # Depuração: Verificar os resultados intermediários do pipeline
#     print("Combos encontrados (pipeline):")
#     for result in results[:5]:  # Limita para verificar alguns resultados
#         print(result)

#     combos_filtrados = []
#     for doc in results:
#         combo = doc["combo"]
#         flat = []
#         for elt in combo:
#             if isinstance(elt, list):
#                 flat.extend(elt)
#             else:
#                 flat.append(elt)
#         pct = doc["count"] / total_wins * 100
#         if pct > 2:
#             combos_filtrados.append({
#                 "combo": flat,
#                 "count": doc["count"],
#                 "percent": round(pct, 2)
#             })

#     return combos_filtrados

# # Teste do código com um intervalo de datas
# data_inicio = datetime(2025, 4, 1)
# data_fim = datetime(2025, 4, 19)
# resultados = executar(data_inicio, data_fim)
# print("Resultados finais:", resultados)


# -0-----

# from datetime import datetime
# from pymongo import MongoClient
# import os
# from dotenv import load_dotenv

# # Carrega as variáveis de ambiente
# load_dotenv()
# client = MongoClient(os.getenv("MONGOKEY"))
# db = client["bd_clashroyale"]
# battles = db["battles"]

# def executar(data_inicio, data_fim):
#     # Convertendo as datas para o formato correto de string com horário
#     start_str = data_inicio.strftime("%Y%m%dT%H%M%S.000Z")
#     end_str = data_fim.strftime("%Y%m%dT%H%M%S.000Z")

#     # Montando o filtro de vitórias
#     match_wins = {
#         "battleTime": {
#             "$gte": start_str,
#             "$lte": end_str
#         },
#         "$expr": {
#             "$gt": [
#                 {"$arrayElemAt": ["$team.crowns", 0]},
#                 {"$arrayElemAt": ["$opponent.crowns", 0]}
#             ]
#         }
#     }

#     # Contando as vitórias no intervalo
#     total_wins = battles.count_documents(match_wins)
    
#     print(f"Procurando vitórias entre: {start_str} e {end_str}")
#     print(f"Total de vitórias encontradas no período: {total_wins}")

#     if total_wins == 0:
#         return []

#     # Pipeline para encontrar combos de cartas com elixirCost >= 1
#     pipeline = [
#         {"$match": match_wins},
#         {"$addFields": {
#             "filtered": {
#                 "$filter": {
#                     "input": "$team.cards",
#                     "as": "c",
#                     "cond": {"$gte": ["$$c.elixirCost", 1]}
#                 }
#             }
#         }},
#         {"$match": {"$expr": {"$gte": [{"$size": "$filtered"}, 1]}}},
#         {"$project": {
#             "combo": {
#                 "$map": {
#                     "input": "$filtered",
#                     "as": "c",
#                     "in": "$$c.name"
#                 }
#             }
#         }},
#         {"$addFields": {
#             "combo": {"$sortArray": {"input": "$combo", "sortBy": 1}}
#         }},
#         {"$group": {
#             "_id": "$combo",
#             "count": {"$sum": 1}
#         }},
#         {"$project": {
#             "_id": 0,
#             "combo": "$_id",
#             "count": 1
#         }}
#     ]

#     # Executando a consulta
#     results = list(battles.aggregate(pipeline))
    
#     combos_filtrados = []
#     for doc in results:
#         combo = doc["combo"]
#         flat = []
#         for elt in combo:
#             if isinstance(elt, list):
#                 flat.extend(elt)
#             else:
#                 flat.append(elt)
#         pct = doc["count"] / total_wins * 100
#         if pct > 2:
#             combos_filtrados.append({
#                 "combo": flat,
#                 "count": doc["count"],
#                 "percent": round(pct, 2)
#             })

#     return combos_filtrados


# ----
# from datetime import datetime
# from pymongo import MongoClient
# import os
# from dotenv import load_dotenv

# load_dotenv()
# client = MongoClient(os.getenv("MONGOKEY"))
# db = client["bd_clashroyale"]
# battles = db["battles"]

# # Definir intervalo de datas
# data_inicio = datetime(2025, 4, 1)
# data_fim = datetime(2025, 4, 19)

# # Converter para string no formato correto
# start_str = data_inicio.strftime("%Y%m%dT%H%M%S.000Z")
# end_str = data_fim.strftime("%Y%m%dT%H%M%S.000Z")

# print("Data início:", start_str)
# print("Data fim:", end_str)

# # Filtro para vitórias (battleTime dentro do intervalo)
# match_wins = {
#     "battleTime": {
#         "$gte": start_str,
#         "$lte": end_str
#     },
#     "$expr": {
#         "$gt": [
#             {"$arrayElemAt": ["$team.crowns", 0]},
#             {"$arrayElemAt": ["$opponent.crowns", 0]}
#         ]
#     }
# }

# # Contar o total de vitórias
# total_wins = battles.count_documents(match_wins)
# print(f"Total de vitórias no período: {total_wins}")

# -- 
# from datetime import datetime
# from pymongo import MongoClient
# import os
# from dotenv import load_dotenv

# load_dotenv()
# client = MongoClient(os.getenv("MONGOKEY"))
# db = client["bd_clashroyale"]
# battles = db["battles"]

# def executar(data_inicio, data_fim):
#     # Converter para string no formato correto
#     start_str = data_inicio.strftime("%Y%m%dT%H%M%S.000Z")
#     end_str = data_fim.strftime("%Y%m%dT%H%M%S.000Z")

#     print("Data início:", start_str)
#     print("Data fim:", end_str)

#     # Filtro para vitórias (battleTime dentro do intervalo)
#     match_wins = {
#         "battleTime": {
#             "$gte": start_str,
#             "$lte": end_str
#         },
#         "$expr": {
#             "$gt": [
#                 {"$arrayElemAt": ["$team.crowns", 0]},
#                 {"$arrayElemAt": ["$opponent.crowns", 0]}
#             ]
#         }
#     }

#     # Contar o total de vitórias
#     total_wins = battles.count_documents(match_wins)
#     print(f"Total de vitórias no período: {total_wins}")

#     if total_wins == 0:
#         print("Nenhuma vitória encontrada.")
#         return []

#     # Pipeline para extrair os combos de cartas
#     pipeline = [
#         {"$match": match_wins},
#         {"$addFields": {
#             "filtered": {
#                 "$filter": {
#                     "input": "$team.cards",
#                     "as": "c",
#                     "cond": {"$gte": ["$$c.elixirCost", 1]}
#                 }
#             }
#         }},
#         {"$match": {"$expr": {"$gte": [{"$size": "$filtered"}, 1]}}},
#         {"$project": {
#             "combo": {
#                 "$map": {
#                     "input": "$filtered",
#                     "as": "c",
#                     "in": "$$c.name"
#                 }
#             }
#         }},
#         {"$addFields": {
#             "combo": {"$sortArray": {"input": "$combo", "sortBy": 1}}
#         }},
#         {"$group": {
#             "_id": "$combo",
#             "count": {"$sum": 1}
#         }},
#         {"$project": {
#             "_id": 0,
#             "combo": "$_id",
#             "count": 1
#         }}
#     ]

#     # Executa a agregação
#     results = list(battles.aggregate(pipeline))

#     print("Resultados da agregação:", results)

#     # Filtrar combos que tenham mais de 2% das vitórias
#     combos_filtrados = []
#     for doc in results:
#         combo = doc["combo"]
#         flat = []
#         for elt in combo:
#             if isinstance(elt, list):
#                 flat.extend(elt)
#             else:
#                 flat.append(elt)
#         pct = doc["count"] / total_wins * 100
#         if pct > 2:
#             combos_filtrados.append({
#                 "combo": flat,
#                 "count": doc["count"],
#                 "percent": round(pct, 2)
#             })

#     return combos_filtrados

# # Teste de execução
# data_inicio = datetime(2025, 4, 1)
# data_fim = datetime(2025, 4, 19)

# resultados = executar(data_inicio, data_fim)
# print("Resultados finais:", resultados)


from datetime import datetime
from main import battles

def executar(data_inicio, data_fim, porcentagem_minima):
    # Converter para string no formato correto
    start_str = data_inicio.strftime("%Y%m%dT%H%M%S.000Z")
    end_str = data_fim.strftime("%Y%m%dT%H%M%S.000Z")

    print("Data início:", start_str)
    print("Data fim:", end_str)

    # Filtro para vitórias (battleTime dentro do intervalo)
    match_wins = {
        "battleTime": {
            "$gte": start_str,
            "$lte": end_str
        },
        "$expr": {
            "$gt": [
                {"$arrayElemAt": ["$team.crowns", 0]},
                {"$arrayElemAt": ["$opponent.crowns", 0]}
            ]
        }
    }

    total_wins = battles.count_documents(match_wins)
    print(f"Total de vitórias no período: {total_wins}")

    if total_wins == 0:
        print("Nenhuma vitória encontrada.")
        return []


    pipeline = [
        {"$match": match_wins},
        {"$addFields": {
            "filtered": {
                "$filter": {
                    "input": "$team.cards",
                    "as": "c",
                    "cond": {"$gte": ["$$c.elixirCost", 1]}
                }
            }
        }},
        {"$match": {"$expr": {"$gte": [{"$size": "$filtered"}, 1]}}},
        {"$project": {
            "combo": {
                "$map": {
                    "input": "$filtered",
                    "as": "c",
                    "in": "$$c.name"
                }
            }
        }},
        {"$addFields": {
            "combo": {"$sortArray": {"input": "$combo", "sortBy": 1}}
        }},
        {"$group": {
            "_id": "$combo",
            "count": {"$sum": 1}
        }},
        {"$project": {
            "_id": 0,
            "combo": "$_id",
            "count": 1
        }}
    ]


    results = list(battles.aggregate(pipeline))

    print("Resultados da agregação:", results)


    combos_filtrados = []
    for doc in results:
        combo = doc["combo"]
        flat = []
        for elt in combo:
            if isinstance(elt, list):
                flat.extend(elt)
            else:
                flat.append(elt)
        pct = doc["count"] / total_wins * 100
        if pct >= porcentagem_minima:
            combos_filtrados.append({
                "combo": flat,
                "count": doc["count"],
                "percent": round(pct, 2)
            })

    return combos_filtrados

data_inicio = datetime(2025, 4, 1)
data_fim = datetime(2025, 4, 19)
porcentagem_minima = 2  

resultados = executar(data_inicio, data_fim, porcentagem_minima)
print("Resultados finais:", resultados)
