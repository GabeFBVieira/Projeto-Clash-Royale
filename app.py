import streamlit as st

st.set_page_config(page_title="Projeto BD Clash Royale", layout="wide")
from datetime import datetime


def importar_consultas():
    from consultas.consulta1 import executar as executar_consulta1
    from consultas.consulta2 import executar as executar_consulta2
    from consultas.consulta3 import executar as executar_consulta3
    from consultas.consulta4 import executar as executar_consulta4
    from consultas.consulta5 import executar as executar_consulta5
    from consultas.consulta_extra1 import executar as executar_consulta_extra1
    from consultas.consulta_extra2 import executar as executar_consulta_extra2
    from consultas.consulta_extra3 import executar as executar_consulta_extra3
    return locals()

consultas = importar_consultas()


st.title("📊 Consultas Clash Royale👑")


tabs = st.tabs([
    "Consulta 1", 
    "Consulta 2", 
    "Consulta 3", 
    "Consulta 4",
    "Consulta 5",
    "Consulta Extra 1",
    "Consulta Extra 2",
    "Consulta Extra 3"

])

# Consulta 1
with tabs[0]:
    st.header("Consulta 1 - % de vitórias e derrotas com carta X")

    cartas_disponiveis = ["Tornado", "Arrows", "Knight", "Musketeer", "Bowler"]
    carta = st.selectbox("Carta:", cartas_disponiveis, index=0, key="c1_carta")
    data_inicio = st.date_input("Data inicial", datetime(2025, 1, 1), key="c1_start")
    data_fim = st.date_input("Data final", datetime(2025, 12, 31), key="c1_end")

    if st.button("Executar Consulta 1", key="btn_c1"):
        with st.spinner("Executando consulta..."):
            resultado = consultas['executar_consulta1'](carta, data_inicio, data_fim)

            if resultado and isinstance(resultado, list) and len(resultado) > 0:
                item = resultado[0]

                vitórias = item.get('vitorias', 0)
                total_batalhas = item.get('total', 0)
                taxa_vitorias = item.get('taxa_vitorias', 0)

                derrotas = total_batalhas - vitórias

                if total_batalhas == 0:
                    st.info("Nenhum dado encontrado para as condições especificadas.")
                else:

                    texto_resultado = f"""
                    Resultados da consulta para a carta '{carta}'

                    Total de batalhas: {total_batalhas}
                    Vitórias: {vitórias} ({taxa_vitorias:.2f}%)
                    Derrotas: {derrotas} ({100 - taxa_vitorias:.2f}%)

                    Período analisado: de {data_inicio} a {data_fim}
                    """
                    st.markdown(texto_resultado) 
            else:
                st.info("Nenhum resultado encontrado para os parâmetros informados.")
   

# Consulta 2
with tabs[1]:

    st.header("Consulta 2 - Decks com mais de X% de vitórias")
    percentual = st.slider("Percentual mínimo de vitórias (%)", 0, 100, 60)
    data_inicio = st.date_input("Data inicial", datetime(2025, 1, 1), key="c2_start")
    data_fim = st.date_input("Data final", datetime(2025, 12, 31), key="c2_end")

    if st.button("Executar Consulta 2", key="btn_c2"):
        resultado = consultas['executar_consulta2'](percentual, data_inicio, data_fim)

        if resultado:
            for i, r in enumerate(resultado, start=1):
                st.markdown(f"""
                ### 🔹 Deck {i}
                **Cartas:** {r["deck"]}
                
                - **Total de Partidas:** `{r["totalPartidas"]}`
                - **Total de Vitórias:** `{r["totalVitorias"]}`
                - **Taxa de Vitórias:** `{r["taxaVitorias"]}%`
                ---
                """)
        else:
            st.warning("Nenhum deck encontrado com o critério informado.")


# Consulta 3
with tabs[2]:
    st.header("Consulta 3 - Derrotas com combo de cartas")

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

#  Consulta 4
with tabs[3]:
    st.header("Consulta 4 - Vitórias com desvantagem de troféus + partida rápida")
    carta = st.text_input("Carta utilizada:", "Golem", key="c4_carta")
    diff_trofeus = st.slider("Desvantagem mínima de troféus (%)", 0, 100, 20)

    if st.button("Executar Consulta 4", key="btn_c4"):
        resultado = consultas['executar_consulta4'](carta, diff_trofeus)
        st.write(f"Quantidade de vitórias: {resultado}")


# Consulta 5
with tabs[4]:
    
    st.header("Consulta 5 - Combos de Cartas com mais de X% de Vitórias")
    st.markdown("Filtra os combos com cartas de elixir ≥ 1 que apareceram em mais de X% das vitórias dentro de um intervalo de tempo.")

    data_inicio = st.date_input("Data inicial", datetime(2025, 4, 1), key="c5_start")
    data_fim = st.date_input("Data final", datetime(2025, 4, 19), key="c5_end")
        
    porcentagem_minima = st.slider(
    "Porcentagem mínima de vitórias (%)",
        min_value=1,
        max_value=100,
        value=2, 
        step=1
    )

    if st.button("Executar Consulta 5", key="btn_c5"):
        st.write(f"Procurando vitórias entre: {data_inicio} e {data_fim}")
        st.write(f"Filtrando combos com mais de {porcentagem_minima}% de vitórias.")

        resultados = consultas['executar_consulta5'](data_inicio, data_fim, porcentagem_minima) 

        if resultados:
            st.write(f"Total de combos encontrados com mais de {porcentagem_minima}% de vitórias: {len(resultados)}")
            for resultado in resultados:
                st.write(f"**Combo**: {', '.join(resultado['combo'])}")
                st.write(f"**Contagem**: {resultado['count']}")
                st.write(f"**Porcentagem**: {resultado['percent']}%")
                st.markdown("---")
        else:
            st.info(f"Nenhum combo encontrado com mais de {porcentagem_minima}% de vitórias.")


# Consulta Extra 1
with tabs[5]:
    st.header("Consulta Extra 1 - Cartas mais utilizadas nos decks")
    
    if st.button("Executar Consulta Extra 1", key="btn_ce1"):
        resultado = consultas['executar_consulta_extra1']()

        if resultado:
            for i, carta in enumerate(resultado, start=1):
                nome_carta = carta.get('card', 'Desconhecido')  
                quantidade = carta.get('count', 0) 
                frequencia = carta.get('percentual', 0.0)  

                if nome_carta != 'Desconhecido' and quantidade > 0:
                    st.markdown(f"""
                    ### 🔹 **{i}. {nome_carta}**
                    - **Quantidade de usos:** {quantidade}
                    - **Frequência nos decks:** {frequencia:.2f}%
                    ---
                    """)
                else:
                    st.markdown(f"🔹 **{i}. Carta com dados incompletos**")
        
        else:
            st.info("Nenhum resultado encontrado.")


# Consulta Extra 2
with tabs[6]:
        st.header("Consulta Extra 2 - Cartas mais usadas por jogadores com 8000+ troféus")
        
        if st.button("Executar Consulta Extra 2", key="btn_ce2"):
            resultado = consultas['executar_consulta_extra2']()

            if resultado:
   
                jogadores = {}
                
                for carta in resultado:
                    jogador = carta.get('Jogador')
                    nome_carta = carta.get('Carta')
                    usos = carta.get('Usos')

                    if jogador not in jogadores:
                        jogadores[jogador] = []

                    jogadores[jogador].append((nome_carta, usos))

                colunas = st.columns(len(jogadores))

                for idx, (jogador, cartas) in enumerate(jogadores.items()):
                    with colunas[idx]:
                        st.markdown(f"### 🏆 **Jogador: {jogador}**")
                        for i, (nome_carta, usos) in enumerate(cartas[:15], start=1):
                            st.markdown(f"""
                            🔹 **{i}. {nome_carta}**
                            - **Quantidade de usos:** {usos}
                            ---
                            """)
            else:
                st.info("Nenhum resultado encontrado.")


# Consulta Extra 3
with tabs[7]:
    st.header("Consulta Extra 3 - Jogadores com maior win rate")
    
    if st.button("Executar Consulta Extra 3", key="btn_ce3"):
        resultado = consultas['executar_consulta_extra3']()

        if resultado:
            st.write("Resultado Final:")
            for i, jogador in enumerate(resultado[:15]): 
                st.write(f"🏆 Jogador: {jogador['name']}")
                st.write(f"🔹 Win Rate: {jogador['winRate']:.2f}%")
        else:
            st.info("Nenhum resultado encontrado.")

