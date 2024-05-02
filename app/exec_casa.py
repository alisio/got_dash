# Referência:
# https://datasaurus-rex.com/inspiration/dsrgallery/gotviz-mkiii

import streamlit as st
import pandas as pd
import altair as alt
import os



deaths_df = pd.read_csv('./data/deaths.csv')

# constantes


img_path = "./img"
principais_personagens = [
    'Arya Stark', 'Cersei Lannister', 'Jon Snow', 'Olenna Tyrell', 'Sansa Stark', 'Tyrion Lannister', 'Bran Stark', 'Daenerys Targaryen', 'Jorah Mormont', 'Robb Stark', 'The High Sparrow', 'game_of_thrones', 'Catelyn Stark', 'Jaime Lannister', 'Littlefinger', 'Samwell Tarly', 'The Hound'
]
principais_personagens.sort()

principais_casas = [
    'House Stark', 'House Lannister', 'House Tyrell', 'House Targaryen', 'House Martell'
]
principais_personagens.sort()

# Variáveis
lista_personagens = list(deaths_df['name'].unique())
lista_personagens.sort()
lista_casa = list(deaths_df['killers_house'].unique())
lista_casa.sort()
top_executores_casa = deaths_df['killers_house'].value_counts().reset_index()
top_executores_casa.columns = ["Executor","Contagem"]
top_metodos_casa = deaths_df['method'].value_counts().reset_index()
top_metodos_casa.columns = ["Metodo","Contagem"]



casa_col1, casa_col2, casa_col3, casa_col4 = st.columns(4)

with casa_col1:
    st.markdown("### Casa:")
    exibe_casas_principais = st.toggle('Somente Principais', key='casa')
    if exibe_casas_principais:
        casa = st.selectbox("Filtro", principais_casas,principais_casas.index('House Stark'))
    else: 
        lista_top_casas_exec_por_num_mortes = list(top_executores_casa['Executor'])
        casa = st.selectbox("Filtro", lista_top_casas_exec_por_num_mortes,lista_top_casas_exec_por_num_mortes.index('House Stark'))

with casa_col2:
    img_arq = f'{img_path}/{casa}.jpeg'    
    st.markdown("### Foto:")
    if os.path.isfile(img_arq):
        st.image(img_arq)
    else:
        st.image("./img/game_of_thrones.png")

with casa_col3:
    num_execucoes = len(deaths_df[deaths_df["killers_house"] == casa ])
    st.markdown("### Execuções:")
    st.markdown(f"## {num_execucoes}")
    
with casa_col4:
    st.markdown("### Métodos:")
    metodos_freq = deaths_df[deaths_df["killers_house"] == casa]["method"].value_counts().reset_index()
    metodos_freq.columns = ["Arma", "Contagem"]
    
    chart_metodos_casa = (
        alt.Chart(metodos_freq[:3]).mark_bar().encode(
            x=alt.X('Arma:N').sort('-y'),
            y=alt.Y('Contagem:Q'),
            color=alt.value('red'),
            # sort=alt.EncodingSortField(field="Contagem", op="count", order='ascending')
        )
    )

    st.altair_chart(chart_metodos_casa, use_container_width=True)


col_body1,col_body2 = st.columns(2)

with col_body1:
    st.image('./img/westeros.jpeg',use_column_width="auto")

with col_body2:
    st.markdown("### Total De Execuções da Casa por Episódio- Cumulativo")
    # Criar df cumulativo
    deaths_df_casa = deaths_df[deaths_df["killers_house"] == casa]
    num_execucoes_por_season_ep = deaths_df_casa.groupby(['season', 'episode']).size().reset_index()
    num_execucoes_por_season_ep.columns = ['Temporada', 'Episódio', 'Execuções']
    num_execucoes_por_season_ep['Cumulativo'] = num_execucoes_por_season_ep['Execuções'].cumsum()
    num_execucoes_por_season_ep['Ep'] = 'S' + num_execucoes_por_season_ep['Temporada'].astype(str) + 'E' + num_execucoes_por_season_ep['Episódio'].astype(str)

    st.line_chart(num_execucoes_por_season_ep,x='Ep',y='Cumulativo',color = '#FF0000')

st.divider()

col_bottom1,col_bottom2 = st.columns(2)
with col_bottom1:
    st.markdown("## Top Executores")

    chart_executores_casa = (
    alt.Chart(top_executores_casa[:10]).mark_bar().encode(
            y=alt.Y('Executor:N').sort('-x'),
            x='Contagem:Q',
            color=alt.value('red'),
            # sort=alt.EncodingSortField(field="Contagem", op="count", order='ascending')
        )
    )

    st.altair_chart(chart_executores_casa, use_container_width=True)


with col_bottom2:
    st.markdown("## Top Métodos")
    chart_metodos_casa = (
        alt.Chart(top_metodos_casa[:10]).mark_bar().encode(
                x='Contagem:Q',
                y=alt.Y('Metodo:N').sort('-x'),
                color=alt.value('red'),
                # sort=alt.EncodingSortField(field="Contagem", op="count", order='ascending')
            )
    )

    st.altair_chart(chart_metodos_casa, use_container_width=True)