# %% [markdown]
# # CD008 Ex02 - Gráficos com a API Altair
# 
# Equipe:
# * Antonio Alisio de Meneses Cordeiro
# * Jeferson Jose de Miranda
# * Salvador Vicente Grisolia

# %% [markdown]
# # Dataset
# 
# Este caderno está focado no dataset de mortes sobre a série de TV Game of Thrones. O enredo fictício dessa série trata da dispuda de poder entre várias famílias e outros agrupamentos ou alianças que nesse caderno vamos chamar de facções. Devido à natureza dessa disputa, várias baixas vão ocorrer ao longo dos episódios. As perguntas que podem surgir nesse sentido envolvem: Qual o personagem que mais causou mortes? Qual foi o método mais utilizado para este fim? Qual casa/facção sofreu mais baixas? Vamos fazer uma análise com o auxílio da biblioteca Altair.
# 
# Disponível em: https://data.world/makeovermonday/2019w27

# %%
# Instalação
# !pip install altair

# %%
# Download do dataset.

# import gdown

# url = 'https://drive.google.com/uc?id=1Eq29Li01ivCukkgOKLbxJYG3RQXG6eL7'
# gdown.download(url, 'deaths.csv')


import os
import requests
import streamlit as st

# Download do dataset.


# %%
import pandas as pd

deaths_df = pd.read_csv('deaths.csv')
# deaths_df

# %% [markdown]
# Nesse dataset temos os nome de quem morreu, sua família/facção, a temporada, o número do episódio, o assassino, a família/facção do assassino, o método do assassinato e a contagem ordenada da morte. Vemos que alguns valoers não estão definidos, vamos resolver isso substituindo NaN por string vazia.

# %%
deaths_df = deaths_df.fillna('')
deaths_df

# %% [markdown]
# # Qual a casa/facção que mais causou mortes?

# %%
import altair as alt

def plotKillerMethod(df, killer_type):
    # Calcular o número de mortes por casa e método
    death_counts = df.groupby([killer_type, 'method']).size().reset_index(name='count')

    # Ordenar os dados pelo número de mortes
    death_counts_sorted = death_counts.sort_values(by='count', ascending=False)

    chart = alt.Chart(death_counts_sorted).mark_bar().encode(
        x=alt.X('count:Q', stack='normalize', axis=alt.Axis(title='Proporção')),
        y=alt.Y(f'{killer_type}:N', sort='-x', axis=alt.Axis(title='Casa do Assassino')),
        color='method:N',
        tooltip=['method', 'count']
    ).properties(
        width=600,
        title=f'Método de Assassinato por ({killer_type}) (Ordenado por Número de Mortes)'
    )

    # Exibir o gráfico
    return chart


st.altair_chart(plotKillerMethod(deaths_df, 'killers_house'), use_container_width=False, theme="streamlit")

# %% [markdown]
# Qualquer um que tenha acompanhado a série sabe o estrago que um dragão consegue fazer. Daí temos a casa Targaryen em primeiro lugar com o maior número de mortes causadas por fogo do dragão. Podemos plotar um gráfico de barras que mostra especificamente quais alianças foram afetadas:

# %%
df_temp = deaths_df[(deaths_df['killers_house']=='House Targaryen') & (deaths_df['method']=='Dragonfire (Dragon)')]
# df_temp

# %%
def deathsByAllegiance(df):
    # Calcular a contagem de alianças por temporada
    counts = df.groupby(['season', 'allegiance']).size().reset_index(name='count')

    # Criar o gráfico de barras empilhadas horizontal com interatividade
    bars = alt.Chart(counts).mark_bar().encode(
        y=alt.Y('season:N', axis=alt.Axis(title='Temporada')),
        x=alt.X('sum(count):Q', axis=alt.Axis(title='Quantidade de Alianças')),
        color=alt.Color('allegiance:N', legend=alt.Legend(title='Aliança')),
        tooltip=['season:N', 'allegiance:N', 'count:Q'],
        row='name:N'
    ).properties(
        width=1000,
        height=400,
        title='Quantidade de Alianças por Temporada'
    ).interactive()

    # Exibir o gráfico
    return bars

deathsByAllegiance(df_temp)
st.altair_chart(deathsByAllegiance(df_temp), use_container_width=False, theme="streamlit")

# %% [markdown]
# E assim vemos que poder dos dragões foi utilizado mais nas últimas temporadas.

# %% [markdown]
# ## Qual o personagem que, individualmente, causou mais mortes?

# %%
# plotKillerMethod(deaths_df, 'killer')
st.altair_chart(plotKillerMethod(deaths_df, 'killer'), use_container_width=False, theme="streamlit")


# %% [markdown]
# Aqui temos com grande destaque Cersei Lannister que matou um grande de pessoas com "fogo selvagem" em um armidilha que ocorreu na sexta temporada:

# %%
df_temp = deaths_df[(deaths_df['killer']=='Cersei Lannister') & (deaths_df['method']=='Wildfire')]
# df_temp

# %%
# deathsByAllegiance(df_temp)
st.altair_chart(deathsByAllegiance(df_temp), use_container_width=False, theme="streamlit")


# %% [markdown]
# # Quem matou quem, usando qual método?

# %%
def plotScatterKill(df):
    # Calcular o número de assassinatos por combinação de 'killer', 'method' e 'location'
    counts = df.groupby(['killer', 'method', 'location']).size().reset_index(name='count')

    # Determinar o tamanho máximo e mínimo de contagem
    max_count = counts['count'].max()
    min_count = counts['count'].min()

    # Definir limites da escala de tamanho
    min_size = 50  # Tamanho mínimo
    max_size = 200  # Tamanho máximo

    # Criar o gráfico de dispersão com escala ajustada
    scatter = alt.Chart(counts).mark_circle().encode(
        x=alt.X('killer:N', axis=alt.Axis(title='Assassino')),
        y=alt.Y('method:N', axis=alt.Axis(title='Método')),
        color='location:N',
        size=alt.Size('count:Q',
                      scale=alt.Scale(domain=[min_count, max_count], range=[min_size, max_size]),
                      legend=alt.Legend(title='Contagem')),
        tooltip=['killer', 'method', 'location', 'count']
    ).properties(
        width=1200,
        height=800,
        title='Relação entre Assassino, Método e Localização'
    ).configure_axis(
        grid=True  # Adicionar grade nos eixos x e y
    ).interactive()

    # Exibir o gráfico
    return scatter

# plotScatterKill(deaths_df)
st.altair_chart(plotScatterKill(deaths_df), use_container_width=False, theme="streamlit")

# %% [markdown]
# # Qual família/facção sofreu mais baixas ao longo das temporadas?

# %%
# deathsByAllegiance(deaths_df)
st.altair_chart(deathsByAllegiance(deaths_df), use_container_width=False, theme="streamlit")

# %%

import streamlit as st



