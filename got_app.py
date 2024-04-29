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

# Download do dataset.

# import gdown

# url = 'https://drive.google.com/uc?id=1Eq29Li01ivCukkgOKLbxJYG3RQXG6eL7'
# gdown.download(url, 'deaths.csv')


import os
import requests
import streamlit as st
import pandas as pd
import altair as alt
import got_lib
from got_lib import plotKillerMethod,deathsByAllegiance,plotScatterKill

deaths_df = pd.read_csv('deaths.csv')

# Nesse dataset temos os nome de quem morreu, sua família/facção, a temporada, o número do episódio, o assassino, a família/facção do assassino, o método do assassinato e a contagem ordenada da morte. Vemos que alguns valoers não estão definidos, vamos resolver isso substituindo NaN por string vazia.

deaths_df = deaths_df.fillna('')

# %%


def pag_dados():
    st.title("Dados")
    # Add code for rendering data and interactivity specific to Page 1
    deaths_df


def pag_execucoes():
    st.title("Execuções:")
    # # Qual a casa/facção que mais causou mortes?
    tipo_execucao = st.selectbox("Execução por: ", ['Indivíduo','Casa'])

    st.tabs(["Casa",["Individuo"]])
    
    if tipo_execucao == 'Indivíduo':
        opcao = 'killer'
    else:
        opcao = 'killers_house'
        
    st.altair_chart(plotKillerMethod(deaths_df, opcao,), use_container_width=False, theme="streamlit")


def pag_alianças():
    # %% [markdown]
    # Qualquer um que tenha acompanhado a série sabe o estrago que um dragão consegue fazer. Daí temos a casa Targaryen em primeiro lugar com o maior número de mortes causadas por fogo do dragão. Podemos plotar um gráfico de barras que mostra especificamente quais alianças foram afetadas:
    
    # %%
    df_temp = deaths_df[(deaths_df['killers_house']=='House Targaryen') & (deaths_df['method']=='Dragonfire (Dragon)')]
    # df_temp
    
    # %%
    
    deathsByAllegiance(df_temp)
    st.altair_chart(deathsByAllegiance(df_temp), use_container_width=False, theme="streamlit")
    
    # %% [markdown]
    # E assim vemos que poder dos dragões foi utilizado mais nas últimas temporadas.
    
    # %% [markdown]
    # ## Qual o personagem que, individualmente, causou mais mortes?
    
    
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
    
    # plotScatterKill(deaths_df)
    st.altair_chart(plotScatterKill(deaths_df), use_container_width=False, theme="streamlit")
    
    # %% [markdown]
    # # Qual família/facção sofreu mais baixas ao longo das temporadas?
    
    # %%
    # deathsByAllegiance(deaths_df)
    st.altair_chart(deathsByAllegiance(deaths_df), use_container_width=False, theme="streamlit")




def app():
    st.title("Os 7 reinos")
    # Set up sidebar menu
    sidebar = st.sidebar
    selected_page = sidebar.selectbox("Selecione Uma Página", ["Dados", "Execuções","Alianças"])

    if selected_page == "Dados":
        pag_dados()
    if selected_page == "Execuções":
        pag_execucoes()
    elif selected_page == "Alianças":
        pag_alianças()
        


def app2():
    st.title("Os 7 reinos")

    # Create tabs for each page using st.tabs()
    tabbed_pages = st.tabs(["Dados", "Execuções","Alianças"])

    with tabbed_pages[0]:
        pag_dados()

    with tabbed_pages[1]:
        pag_execucoes()
    
    with tabbed_pages[2]:
        pag_alianças()


app()



