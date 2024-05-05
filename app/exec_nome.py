# Referência:
# https://datasaurus-rex.com/inspiration/dsrgallery/gotviz-mkiii

import streamlit as st
import pandas as pd
import altair as alt
import os



deaths_df = pd.read_csv('./data/deaths.csv')

# constantes
img_path = "./img"
largura_imagens = 200
principais_personagens = [
    'Arya Stark', 'Cersei Lannister', 'Jon Snow', 'Olenna Tyrell', 'Sansa Stark', 'Tyrion Lannister', 'Bran Stark', 'Daenerys Targaryen', 'Jorah Mormont', 'Robb Stark', 'The High Sparrow', 'Catelyn Stark', 'Jaime Lannister', 'Littlefinger', 'Samwell Tarly', 'The Hound'
]
principais_personagens.sort()

texto_sidebar = """
# Descrição
Este dashboard está focado no dataset de mortes sobre a série de TV Game of Thrones. O enredo fictício dessa série trata da dispuda de poder entre várias famílias e outros agrupamentos ou alianças que nesse caderno vamos chamar de facções. Devido à natureza dessa disputa, várias baixas vão ocorrer ao longo dos episódios. As perguntas que podem surgir nesse sentido envolvem: 

* Qual o personagem que mais causou mortes? 
* Qual foi o método mais utilizado para este fim? 
* Qual aliança sofreu mais baixas? 

Vamos fazer uma análise com o auxílio da biblioteca streamlit.

# Código fonte:
https://github.com/alisio/got_dash

# Reconhecimentos:
* [Game of Thrones Datasets and Visualizations](https://github.com/jeffreylancaster/game-of-thrones)
* Wikipedia


"""


# Variáveis
lista_personagens = list(deaths_df['name'].unique())
lista_personagens.sort()
top_executores = deaths_df['killer'].value_counts().reset_index()
top_executores.columns = ["Executor","Contagem"]
top_metodos = deaths_df['method'].value_counts().reset_index()
top_metodos.columns = ["Metodo","Contagem"]

# Página

st.sidebar.write(texto_sidebar)

pers_col1, pers_col2, pers_col3, pers_col4 = st.columns(4)

with pers_col1:
    st.markdown("### Personagem:")
    exibe_personagem_principais = st.toggle('Somente Principais', key='nome_executor')
    if exibe_personagem_principais:
        personagem = st.selectbox("Filtro", principais_personagens,principais_personagens.index('Jon Snow'))
    else: 
        lista_top_exec_por_num_mortes = list(top_executores['Executor'])
        personagem = st.selectbox("Filtro", lista_top_exec_por_num_mortes,lista_top_exec_por_num_mortes.index('Jon Snow'))

with pers_col2:
    img_arq = f'{img_path}/{personagem.replace(" ","-")}.webp'    
    st.markdown("### Foto:")
    if os.path.isfile(img_arq):
        st.image(img_arq, width=largura_imagens)
    else:
        st.image("./img/game_of_thrones.png")

with pers_col3:
    num_execucoes = len(deaths_df[deaths_df["killer"] == personagem ])
    casa = list(deaths_df[deaths_df["killer"] == personagem ]['killers_house'].unique())
    st.markdown("### Execuções:")
    st.markdown(f"## {num_execucoes}")
    st.markdown("### Aliança:")
    for i in casa:
        # st.markdown(', '.join(casa))
        st.markdown(f"- {i}")
        # st.image(f"{img_path}/{i}.jpeg",width=50)
    
with pers_col4:
    st.markdown("### Métodos (Top 3):")
    metodos_freq = deaths_df[deaths_df["killer"] == personagem]["method"].value_counts().reset_index()
    metodos_freq.columns = ["Arma", "Contagem"]
    
    chart_metodos = (
        alt.Chart(metodos_freq[:3]).mark_bar().encode(
            x=alt.X('Arma:N').sort('-y'),
            y=alt.Y('Contagem:Q'),
            color=alt.value('red'),
            # sort=alt.EncodingSortField(field="Contagem", op="count", order='ascending')
        )
    )

    st.altair_chart(chart_metodos, use_container_width=True)

# col_body1,col_body2 = st.columns(2)

# with col_body1:
    # st.image('./img/westeros.jpeg',use_column_width="auto")

# with col_body2:
st.markdown("### Total De Execuções do Personagem - Cumulativo")
# Criar df cumulativo
deaths_df_personagem = deaths_df[deaths_df["killer"] == personagem]
num_execucoes_por_season_ep = deaths_df_personagem.groupby(['season', 'episode']).size().reset_index()
num_execucoes_por_season_ep.columns = ['Temporada', 'Episódio', 'Execuções']
num_execucoes_por_season_ep['Temporada'] = num_execucoes_por_season_ep['Temporada'].astype(str).apply(lambda x: x.zfill(2))
num_execucoes_por_season_ep['Episódio'] = num_execucoes_por_season_ep['Episódio'].astype(str).apply(lambda x: x.zfill(2))
num_execucoes_por_season_ep['Cumulativo'] = num_execucoes_por_season_ep['Execuções'].cumsum()
num_execucoes_por_season_ep['Ep'] = 'S' + num_execucoes_por_season_ep['Temporada'] + 'E' + num_execucoes_por_season_ep['Episódio']

# Criar um DF contendo todas as temporadas e episódios em formato S0XE0Y
df_ep = deaths_df[['season','episode']].copy()
df_ep['season'] = df_ep['season'].astype(str).apply(lambda x: x.zfill(2))
df_ep['episode'] = df_ep['episode'].astype(str).apply(lambda x: x.zfill(2))
df_ep['Ep'] = 'S' + df_ep['season'] + 'E' + df_ep['episode']
df_ep = df_ep.drop_duplicates()

df_exec_cum = pd.merge(df_ep['Ep'],num_execucoes_por_season_ep,'outer','Ep')
df_exec_cum['Execuções'] = df_exec_cum['Execuções'].ffill()
df_exec_cum['Cumulativo'] = df_exec_cum['Cumulativo'].ffill()

st.line_chart(df_exec_cum,x='Ep',y='Cumulativo',color = '#FF0000')

st.divider()


st.columns(3)[1].markdown("## Top 10 Geral")

col_bottom1,col_bottom2 = st.columns(2)
with col_bottom1:
    st.markdown("### Executores")

    chart_executores = (
    alt.Chart(top_executores[:10]).mark_bar().encode(
            y=alt.Y('Executor:N').sort('-x'),
            x='Contagem:Q',
            color=alt.value('red'),
            # sort=alt.EncodingSortField(field="Contagem", op="count", order='ascending')
        )
    )

    st.altair_chart(chart_executores, use_container_width=True)


with col_bottom2:
    st.markdown("### Top Métodos")
    chart_metodos = (
        alt.Chart(top_metodos[:10]).mark_bar().encode(
                x='Contagem:Q',
                y=alt.Y('Metodo:N').sort('-x'),
                color=alt.value('red'),
                # sort=alt.EncodingSortField(field="Contagem", op="count", order='ascending')
            )
    )

    st.altair_chart(chart_metodos, use_container_width=True)