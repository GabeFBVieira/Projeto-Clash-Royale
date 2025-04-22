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

# import streamlit as st
# from datetime import datetime, time
# from main import battles

# def executar(percentual: float, data_inicio: datetime, data_fim: datetime):
    
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
#                 "battleTimeDate": {
#                     "$gte": datetime.combine(data_inicio, time(0, 0, 0)),
#                     "$lte": datetime.combine(data_fim, time(23, 59, 59, 999000))
#                 }
#             }
#         },
#         {
#             "$addFields": {
#                 "vitoria": {
#                     "$gt": [
#                         { "$arrayElemAt": ["$team.crowns", 0] },
#                         { "$max": "$opponent.crowns" }
#                     ]
#                 }
#             }
#         },
#         {
#             "$group": {
#                 "_id": "$team.cards",
#                 "totalPartidas": { "$sum": 1 },
#                 "totalVitorias": {
#                     "$sum": {
#                         "$cond": ["$vitoria", 1, 0]
#                     }
#                 }
#             }
#         },
#         {
#             "$addFields": {
#                 "taxaVitorias": {
#                     "$multiply": [
#                         { "$divide": ["$totalVitorias", "$totalPartidas"] },
#                         100
#                     ]
#                 }
#             }
#         },
#         {
#             "$match": {
#                 "taxaVitorias": { "$gte": percentual }
#             }
#         },
#         {
#             "$project": {
#                 "_id": 0,
#                 "deck": "$_id",
#                 "totalPartidas": 1,
#                 "totalVitorias": 1,
#                 "taxaVitorias": { "$round": ["$taxaVitorias", 2] }
#             }
#         },
#         { "$sort": { "taxaVitorias": -1 } }
#     ]
#     brutos = list(battles.aggregate(pipeline))
       
#     resultados = []
#     for r in brutos:
#         # Pega as cartas e extrai apenas os nomes
#         nomes_cartas = [carta.get('name', 'Desconhecido') for carta in r.get('deck', [])]
        
#         # Adiciona os resultados ao final
#         resultados.append({
#             "deck": ", ".join(nomes_cartas),
#             "totalPartidas": r.get("totalPartidas", 0),
#             "totalVitorias": r.get("totalVitorias", 0),
#             "taxaVitorias": r.get("taxaVitorias", 0.0)
#         })

#     return resultados

# --------------------------------

# import streamlit as st
# from datetime import datetime, time
# from main import battles

# def executar(percentual: float, data_inicio: datetime, data_fim: datetime):
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
#                 "battleTimeDate": {
#                     "$gte": datetime.combine(data_inicio, time(0, 0, 0)),
#                     "$lte": datetime.combine(data_fim, time(23, 59, 59, 999000))
#                 }
#             }
#         },
#         {
#             "$addFields": {
#                 "vitoria": {
#                     "$gt": [
#                         { "$arrayElemAt": ["$team.crowns", 0] },
#                         { "$max": "$opponent.crowns" }
#                     ]
#                 }
#             }
#         },
#         {
#             "$group": {
#                 "_id": "$team.cards",
#                 "totalPartidas": { "$sum": 1 },
#                 "totalVitorias": {
#                     "$sum": {
#                         "$cond": ["$vitoria", 1, 0]
#                     }
#                 }
#             }
#         },
#         {
#             "$addFields": {
#                 "taxaVitorias": {
#                     "$multiply": [
#                         { "$divide": ["$totalVitorias", "$totalPartidas"] },
#                         100
#                     ]
#                 }
#             }
#         },
#         {
#             "$match": {
#                 "taxaVitorias": { "$gte": percentual }
#             }
#         },
#         {
#             "$project": {
#                 "_id": 0,
#                 "deck": "$_id",
#                 "totalPartidas": 1,
#                 "totalVitorias": 1,
#                 "taxaVitorias": { "$round": ["$taxaVitorias", 2] }
#             }
#         },
#         { "$sort": { "taxaVitorias": -1 } }
#     ]

#     # Resultados da consulta no MongoDB
#     brutos = list(battles.aggregate(pipeline))
    
#     # Processamento dos resultados
#     resultados = []
#     for r in brutos:
#         # Verificar se o campo 'deck' existe e processar as cartas
#         if 'deck' not in r:
#             print("Campo 'deck' ausente em:", r)
#             continue
        
#         nomes_cartas = []
#         for carta in r['deck']:  # 'deck' contém os objetos das cartas
#             # Acessar o nome da carta dentro de cada objeto
#             nome_carta = carta.get('name', 'Desconhecido')
#             nomes_cartas.append(nome_carta)
        
#         resultados.append({
#             "deck": ", ".join(nomes_cartas),
#             "totalPartidas": r.get("totalPartidas", 0),
#             "totalVitorias": r.get("totalVitorias", 0),
#             "taxaVitorias": r.get("taxaVitorias", 0.0)
#         })

#     return resultados
# ----------------------------------------

# import streamlit as st
# from datetime import datetime, time
# from main import battles

# def executar(percentual: float, data_inicio: datetime, data_fim: datetime):
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
#                 "battleTimeDate": {
#                     "$gte": datetime.combine(data_inicio, time(0, 0, 0)),
#                     "$lte": datetime.combine(data_fim, time(23, 59, 59, 999000))
#                 }
#             }
#         },
#         {
#             "$addFields": {
#                 "vitoria": {
#                     "$gt": [
#                         { "$arrayElemAt": ["$team.crowns", 0] },
#                         { "$max": "$opponent.crowns" }
#                     ]
#                 }
#             }
#         },
#         {
#             "$group": {
#                 "_id": "$team.cards",
#                 "totalPartidas": { "$sum": 1 },
#                 "totalVitorias": {
#                     "$sum": {
#                         "$cond": ["$vitoria", 1, 0]
#                     }
#                 }
#             }
#         },
#         {
#             "$addFields": {
#                 "taxaVitorias": {
#                     "$multiply": [
#                         { "$divide": ["$totalVitorias", "$totalPartidas"] },
#                         100
#                     ]
#                 }
#             }
#         },
#         {
#             "$match": {
#                 "taxaVitorias": { "$gte": percentual }
#             }
#         },
#         {
#             "$project": {
#                 "_id": 0,
#                 "deck": "$_id",
#                 "totalPartidas": 1,
#                 "totalVitorias": 1,
#                 "taxaVitorias": { "$round": ["$taxaVitorias", 2] }
#             }
#         },
#         { "$sort": { "taxaVitorias": -1 } }
#     ]

#     # Resultados da consulta no MongoDB
#     brutos = list(battles.aggregate(pipeline))
    
#     # Processamento dos resultados
#     resultados = []
#     for r in brutos:
#         # Verificar se o campo 'deck' existe e é uma lista
#         if 'deck' in r and isinstance(r['deck'], list):
#             nomes_cartas = []
#             for carta in r['deck']:  # 'deck' contém os objetos das cartas
#                 # Acessar o nome da carta dentro de cada objeto
#                 nome_carta = carta.get('name', 'Desconhecido')
#                 nomes_cartas.append(nome_carta)
            
#             resultados.append({
#                 "deck": ", ".join(nomes_cartas),
#                 "totalPartidas": r.get("totalPartidas", 0),
#                 "totalVitorias": r.get("totalVitorias", 0),
#                 "taxaVitorias": r.get("taxaVitorias", 0.0)
#             })
#         else:
#             print("Erro: 'deck' não encontrado ou não é uma lista válida em:", r)

#     return resultados

#----------------------------------

# import streamlit as st
# from datetime import datetime, time
# from main import battles

# def executar(percentual: float, data_inicio: datetime, data_fim: datetime):
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
#                 "battleTimeDate": {
#                     "$gte": datetime.combine(data_inicio, time(0, 0, 0)),
#                     "$lte": datetime.combine(data_fim, time(23, 59, 59, 999000))
#                 }
#             }
#         },
#         {
#             "$addFields": {
#                 "vitoria": {
#                     "$gt": [
#                         { "$arrayElemAt": ["$team.crowns", 0] },
#                         { "$max": "$opponent.crowns" }
#                     ]
#                 }
#             }
#         },
#         {
#             "$group": {
#                 "_id": "$team.cards",
#                 "totalPartidas": { "$sum": 1 },
#                 "totalVitorias": {
#                     "$sum": {
#                         "$cond": ["$vitoria", 1, 0]
#                     }
#                 }
#             }
#         },
#         {
#             "$addFields": {
#                 "taxaVitorias": {
#                     "$multiply": [
#                         { "$divide": ["$totalVitorias", "$totalPartidas"] },
#                         100
#                     ]
#                 }
#             }
#         },
#         {
#             "$match": {
#                 "taxaVitorias": { "$gte": percentual }
#             }
#         },
#         {
#             "$project": {
#                 "_id": 0,
#                 "deck": "$_id",
#                 "totalPartidas": 1,
#                 "totalVitorias": 1,
#                 "taxaVitorias": { "$round": ["$taxaVitorias", 2] }
#             }
#         },
#         { "$sort": { "taxaVitorias": -1 } }
#     ]

#     # Resultados da consulta no MongoDB
#     brutos = list(battles.aggregate(pipeline))
    
#     # Processamento dos resultados
#     resultados = []
#     for r in brutos:
#         # Verificar se o campo 'deck' existe e é uma lista
#         if 'deck' in r and isinstance(r['deck'], list):
#             nomes_cartas = []
#             for carta in r['deck']:  # 'deck' contém os objetos das cartas
#                 if isinstance(carta, dict):  # Verificar se carta é um dicionário
#                     nome_carta = carta.get('name', 'Desconhecido')
#                     nomes_cartas.append(nome_carta)
#                 else:
#                     print(f"Erro: 'carta' não é um dicionário: {carta}")
            
#             resultados.append({
#                 "deck": ", ".join(nomes_cartas),
#                 "totalPartidas": r.get("totalPartidas", 0),
#                 "totalVitorias": r.get("totalVitorias", 0),
#                 "taxaVitorias": r.get("taxaVitorias", 0.0)
#             })
#         else:
#             print(f"Erro: 'deck' não encontrado ou não é uma lista válida em: {r}")

#     return resultados


#------- funcionou, mas é muito complexo----
# import streamlit as st
# from datetime import datetime, time
# from main import battles

# def executar(percentual: float, data_inicio: datetime, data_fim: datetime):
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
#                 "battleTimeDate": {
#                     "$gte": datetime.combine(data_inicio, time(0, 0, 0)),
#                     "$lte": datetime.combine(data_fim, time(23, 59, 59, 999000))
#                 }
#             }
#         },
#         {
#             "$addFields": {
#                 "vitoria": {
#                     "$gt": [
#                         { "$arrayElemAt": ["$team.crowns", 0] },
#                         { "$max": "$opponent.crowns" }
#                     ]
#                 }
#             }
#         },
#         {
#             "$group": {
#                 "_id": "$team.cards",
#                 "totalPartidas": { "$sum": 1 },
#                 "totalVitorias": {
#                     "$sum": {
#                         "$cond": ["$vitoria", 1, 0]
#                     }
#                 }
#             }
#         },
#         {
#             "$addFields": {
#                 "taxaVitorias": {
#                     "$multiply": [
#                         { "$divide": ["$totalVitorias", "$totalPartidas"] },
#                         100
#                     ]
#                 }
#             }
#         },
#         {
#             "$match": {
#                 "taxaVitorias": { "$gte": percentual }
#             }
#         },
#         {
#             "$project": {
#                 "_id": 0,
#                 "deck": "$_id",
#                 "totalPartidas": 1,
#                 "totalVitorias": 1,
#                 "taxaVitorias": { "$round": ["$taxaVitorias", 2] }
#             }
#         },
#         { "$sort": { "taxaVitorias": -1 } }
#     ]
    
#     # Resultados da consulta no MongoDB
#     brutos = list(battles.aggregate(pipeline))
    
#     # Inicializando resultados
#     resultados = []
#     for r in brutos:
#         # Verificando se 'deck' existe e é uma lista
#         if 'deck' in r and isinstance(r['deck'], list):
#             nomes_cartas = []
#             for carta in r['deck']:  # Cada carta pode ser uma lista ou dicionário
#                 # Examinando a estrutura interna de cada carta
#                 if isinstance(carta, dict):
#                     # Caso a carta seja um dicionário
#                     nome_carta = carta.get('name', 'Desconhecido')
#                     nomes_cartas.append(nome_carta)
#                 elif isinstance(carta, list):
#                     # Caso a carta seja uma lista (verificação para tratamento adequado)
#                     for item in carta:  # Caso seja uma lista dentro da carta
#                         if isinstance(item, dict):
#                             nome_carta = item.get('name', 'Desconhecido')
#                             nomes_cartas.append(nome_carta)
#             resultados.append({
#                 "deck": ", ".join(nomes_cartas),
#                 "totalPartidas": r.get("totalPartidas", 0),
#                 "totalVitorias": r.get("totalVitorias", 0),
#                 "taxaVitorias": r.get("taxaVitorias", 0.0)
#             })
#         else:
#             print(f"Erro: 'deck' não encontrado ou não é uma lista válida em: {r}")
    
#     return resultados

# ------- TA FUNCIONANDO CACILDIS, E SIMPLIFICADO HEHE-----

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


    





































# import streamlit as st
# from datetime import datetime
# from main import battles
# import stfront

# # Função de consulta adaptada para o Streamlit
# def consultar_decks(percentual, data_inicio, data_fim):
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
#                 "battleTimeDate": {
#                     "$gte": datetime.combine(data_inicio, datetime.min.time()),
#                     "$lte": datetime.combine(data_fim, datetime.max.time())
#                 }
#             }
#         },
#         {
#             "$addFields": {
#                 "vitoria": {
#                     "$gt": [
#                         { "$arrayElemAt": ["$team.crowns", 0] },
#                         { "$max": "$opponent.crowns" }
#                     ]
#                 }
#             }
#         },
#         {
#             "$group": {
#                 "_id": "$team.cards",
#                 "totalPartidas": { "$sum": 1 },
#                 "totalVitorias": {
#                     "$sum": {
#                         "$cond": ["$vitoria", 1, 0]
#                     }
#                 }
#             }
#         },
#         {
#             "$addFields": {
#                 "taxaVitorias": {
#                     "$multiply": [
#                         { "$divide": ["$totalVitorias", "$totalPartidas"] },
#                         100
#                     ]
#                 }
#             }
#         },
#         {
#             "$match": {
#                 "taxaVitorias": { "$gte": percentual }
#             }
#         },
#         {
#             "$project": {
#                 "_id": 0,
#                 "deck": "$_id",
#                 "totalPartidas": 1,
#                 "totalVitorias": 1,
#                 "taxaVitorias": { "$round": ["$taxaVitorias", 2] }
#             }
#         },
#         { "$sort": { "taxaVitorias": -1 } }
#     ]
#     resultados = list(battles.aggregate(pipeline))
#     return resultados

# # # Streamlit
# st.title("📊 Consulta de Decks com Maior Taxa de Vitórias")

# # Chama o stfront para pegar os valores dos parâmetros
# percentual = stfront.percentual  # Supondo que o stfront tem essa variável já configurada
# data_inicio = stfront.data_inicio  # Supondo que o stfront tem essa variável já configurada
# data_fim = stfront.data_fim  # Supondo que o stfront tem essa variável já configurada

# # Botão para executar a consulta
# if stfront.executar_consulta:  # E você precisa ter esse botão configurado no stfront
#     with st.spinner("Executando consulta..."):
#         resultados = consultar_decks(percentual, data_inicio, data_fim)
#         if resultados:
#             for r in resultados:
#                 deck_nomes = []
#                 for cards in r['deck']:  
#                     for card in cards[:8]:  
#                         deck_nomes.append(card.get('name', 'Desconhecido'))
#                 deck_str = ", ".join(deck_nomes[:8])
#                 st.write(f"**Deck:** {deck_str}")
#                 st.write(f"**Total de Partidas:** {r['totalPartidas']}")
#                 st.write(f"**Total de Vitórias:** {r['totalVitorias']}")
#                 st.write(f"**Taxa de Vitórias:** {r['taxaVitorias']}%")
#                 st.markdown("---")
#         else:
#             st.info("Nenhum resultado encontrado para os parâmetros informados.")

