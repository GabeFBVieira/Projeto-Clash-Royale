import streamlit as st

st.set_page_config(page_title="Projeto BD Clash Royale", layout="wide")
from datetime import datetime




# Importações das funções de cada consulta
def importar_consultas():
    from consultas.consulta1 import executar as executar_consulta1
    from consultas.consulta2 import executar as executar_consulta2
    from consultas.consulta3 import executar as executar_consulta3
    # from consultas.consulta4 import executar as executar_consulta4
    # from consultas.consulta5 import executar as executar_consulta5
    # from consultas.consulta_extra1 import executar as executar_consulta_extra1
    # from consultas.consulta_extra2 import executar as executar_consulta_extra2
    # from consultas.consulta_extra3 import executar as executar_consulta_extra3
    return locals()

consultas = importar_consultas()



# Configuração da página
st.title("📊 Consultas Clash Royale👑")

# Tabs
tabs = st.tabs([
    "Consulta 1", 
    "Consulta 2", 
    "Consulta 3", 
    # "Consulta 4",
    # "Consulta 5",
    # "Consulta Extra 1",
    # "Consulta Extra 2",
    # "Consulta Extra 3"
])

# Consulta 1
with tabs[0]:
    st.header("Consulta 1 - % de vitórias e derrotas com carta X")
    carta = st.text_input("Carta:", "Musketeer", key="c1_carta")
    data_inicio = st.date_input("Data inicial", datetime(2025, 1, 1), key="c1_start")
    data_fim = st.date_input("Data final", datetime(2025, 12, 31), key="c1_end")

    if st.button("Executar Consulta 1", key="btn_c1"):
        with st.spinner("Executando consulta..."):
            resultado = consultas['executar_consulta1'](carta, data_inicio, data_fim)
            if resultado:
                st.dataframe(resultado)
            else:
                st.info("Nenhum resultado encontrado para os parâmetros informados.")

# Consulta 2
with tabs[1]:
    st.header("Consulta 2 - Decks com mais de X% de vitórias")
    percentual = st.slider("Percentual mínimo de vitórias (%)", 0, 100, 60)
    data_inicio = st.date_input("Data inicial", datetime(2024, 1, 1), key="c2_start")
    data_fim = st.date_input("Data final", datetime(2024, 12, 31), key="c2_end")

    if st.button("Executar Consulta 2", key="btn_c2"):
        resultado = consultas['executar_consulta2'](percentual, data_inicio, data_fim)
        st.dataframe(resultado)

# with tabs[1]:
#     st.header("Consulta 2 - Decks com mais de X% de vitórias")
    
#     # Verifique os parâmetros
#     percentual = st.slider("Percentual mínimo de vitórias (%)", 0, 100, 60)
#     data_inicio = st.date_input("Data inicial", datetime(2024, 1, 1), key="c2_start")
#     data_fim = st.date_input("Data final", datetime(2024, 12, 31), key="c2_end")
 
#     if st.button("Executar Consulta 2", key="btn_c2"):     
#         # Chama a consulta e passa os parâmetros corretos
#         resultado = consultas['executar_consulta2'](percentual, data_inicio, data_fim)
#         st.dataframe(resultado)
#         if not resultado:
#                 st.warning("Nenhum resultado retornado pela consulta.")
#         else:
#             st.success(f"{len(resultado)} resultados encontrados.")
#             for r in resultado:
#                 st.write(r)

# Consulta 3
with tabs[2]:
    st.header("Consulta 3 - Derrotas com combo de cartas")

    # Combo fixo para: Musketeer, Skeletons, Miner
    cartas = ["Musketeer", "Skeletons", "Miner"]
    st.write(f"Combo de cartas fixo: {', '.join(cartas)}")

    data_inicio = st.date_input("Data inicial", datetime(2025, 1, 1), key="c3_start")
    data_fim = st.date_input("Data final", datetime(2025, 12, 31), key="c3_end")

    if st.button("Executar Consulta 3", key="btn_c3"):
        resultado = consultas['executar_consulta3'](cartas, data_inicio, data_fim)
        if resultado:
            for r in resultado:
                st.write(f"**Total de Partidas:** {r['totalPartidas']}")
                st.write(f"**Total de Derrotas:** {r['totalDerrotas']}")
                st.write(f"**Taxa de Derrotas:** {r['taxaDerrotas']}%")
                st.markdown("---")
        else:
            st.info("Nenhum resultado encontrado para os parâmetros informados.")


# # Consulta 4
# with tabs[3]:
#     st.header("Consulta 4 - Vitórias com desvantagem de troféus + partida rápida")
#     carta = st.text_input("Carta utilizada:", "Golem", key="c4_carta")
#     diff_trofeus = st.slider("Desvantagem mínima de troféus (%)", 0, 100, 20)

#     if st.button("Executar Consulta 4", key="btn_c4"):
#         resultado = consultas['executar_consulta4'](carta, diff_trofeus)
#         st.write(f"Quantidade de vitórias: {resultado}")

# # Consulta 5
# with tabs[4]:
#     st.header("Consulta 5 - [Descrição da Consulta 5]")
#     # Adicione aqui inputs necessários para consulta 5
#     if st.button("Executar Consulta 5", key="btn_c5"):
#         resultado = consultas['executar_consulta5']()
#         st.dataframe(resultado)

# # Consulta Extra 1
# with tabs[5]:
#     st.header("Consulta Extra 1 - Cartas mais utilizadas nos decks")
#     if st.button("Executar Consulta Extra 1", key="btn_ce1"):
#         resultado = consultas['executar_consulta_extra1']()
#         st.dataframe(resultado)

# # Consulta Extra 2
# with tabs[6]:
#     st.header("Consulta Extra 2 - [Descrição da Consulta Extra 2]")
#     if st.button("Executar Consulta Extra 2", key="btn_ce2"):
#         resultado = consultas['executar_consulta_extra2']()
#         st.dataframe(resultado)

# # Consulta Extra 3
# with tabs[7]:
#     st.header("Consulta Extra 3 - [Descrição da Consulta Extra 3]")
#     if st.button("Executar Consulta Extra 3", key="btn_ce3"):
#         resultado = consultas['executar_consulta_extra3']()
#         st.dataframe(resultado)