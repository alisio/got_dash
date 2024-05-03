import os
import requests
import streamlit as st
import pandas as pd
import altair as alt
import got_lib
from got_lib import plotKillerMethod,deathsByAllegiance,plotScatterKill
import sys


deaths_df = pd.read_csv('./data/deaths.csv')

# Nesse dataset temos os nome de quem morreu, sua família/facção, a temporada, o número do episódio, o assassino, a família/facção do assassino, o método do assassinato e a contagem ordenada da morte. Vemos que alguns valoers não estão definidos, vamos resolver isso substituindo NaN por string vazia.

deaths_df = deaths_df.fillna('')

# %%


def pag_dados():
    # st.title("Dados")
    # Add code for rendering data and interactivity specific to Page 1
    # deaths_df
    tabbed_pages = st.tabs(["Executor", "Casa"])

    with tabbed_pages[0]:
        import exec_nome
        del sys.modules['exec_nome']

    with tabbed_pages[1]:
        import exec_casa
        del sys.modules['exec_casa']


def pag_execucoes():
    st.title("Execuções:")
    # # Qual a casa/facção que mais causou mortes?
    # tipo_execucao = st.selectbox("Execução por: ", ['Indivíduo','Casa'])

    aba_exec_casa,aba_exec_individuo,aba_exec_relacionamento = st.tabs(["Casa","Individuo","Relacionamento"])
    with aba_exec_casa:
        opcao = 'killers_house'
        print(opcao)
        st.altair_chart(plotKillerMethod(deaths_df, opcao,), use_container_width=True, theme="streamlit")
    with aba_exec_individuo:
        opcao = 'killer'
        st.altair_chart(plotKillerMethod(deaths_df, opcao,), use_container_width=True, theme="streamlit")
    with aba_exec_relacionamento:
        nomes = list(deaths_df['name'].unique())
        assassinos = list(deaths_df['killer'].unique())
        locais = list(deaths_df['location'].unique())
        metodos = list(deaths_df['method'].unique())
        # vitima = st.multiselect('Seleção de Vítimas',nomes)
        # assassino = st.multiselect('Seleção de Assassínos',assassinos)
        # localizacao = st.multiselect('Seleção de Locais',locais)
        # metodo = st.multiselect('Seleção de Métodos',metodos)
        # Create four columns with equal width
        col1, col2, col3, col4 = st.columns(4)
        
        # Assign each Streamlit object to a separate column
        with col1:
            vitima = st.multiselect('Seleção de Vítimas', nomes)
        with col2:
            assassino = st.multiselect('Seleção de Assassínos', assassinos)
        with col3:
            localizacao = st.multiselect('Seleção de Locais', locais)
        with col4:
            metodo = st.multiselect('Seleção de Métodos', metodos)
        
        df_exec_tmp = deaths_df[deaths_df['name'].isin(vitima)]
        st.altair_chart(plotScatterKill(df_exec_tmp), use_container_width=False, theme="streamlit")

        
        
    


def pag_alianças():
    # %% [markdown]
    # Qualquer um que tenha acompanhado a série sabe o estrago que um dragão consegue fazer. Daí temos a casa Targaryen em primeiro lugar com o maior número de mortes causadas por fogo do dragão. Podemos plotar um gráfico de barras que mostra especificamente quais alianças foram afetadas:

    df_temp = deaths_df[(deaths_df['killers_house']=='House Targaryen') & (deaths_df['method']=='Dragonfire (Dragon)')]

    aba_alianca_casa,aba_alianca_individuo = st.tabs(["Casa","Individuo"])
    with aba_alianca_casa:
        st.altair_chart(deathsByAllegiance(deaths_df), use_container_width=False, theme="streamlit")
    with aba_alianca_individuo:
        opcao = 'killer'

    
    # %%
    df_temp = deaths_df[(deaths_df['killers_house']=='House Targaryen') & (deaths_df['method']=='Dragonfire (Dragon)')]
    # df_temp
    
    # %%
    
    # deathsByAllegiance(df_temp)
    # st.altair_chart(deathsByAllegiance(df_temp), use_container_width=False, theme="streamlit")
    
    # %% [markdown]
    # E assim vemos que poder dos dragões foi utilizado mais nas últimas temporadas.
    
    # %% [markdown]
    # ## Qual o personagem que, individualmente, causou mais mortes?
    
    
    # %% [markdown]
    # Aqui temos com grande destaque Cersei Lannister que matou um grande de pessoas com "fogo selvagem" em um armidilha que ocorreu na sexta temporada:
    
    # %%
    df_temp = deaths_df[(deaths_df['killer']=='Cersei Lannister') & (deaths_df['method']=='Wildfire')]
    # df_temp
    
    # %% [markdown]
    # # Quem matou quem, usando qual método?
    
    # %%
    
    # plotScatterKill(deaths_df)
    # st.altair_chart(plotScatterKill(deaths_df), use_container_width=False, theme="streamlit")
    
    # %% [markdown]
    # # Qual família/facção sofreu mais baixas ao longo das temporadas?
    
    # %%
    # deathsByAllegiance(deaths_df)
    st.altair_chart(deathsByAllegiance(deaths_df), use_container_width=False, theme="streamlit")




def app():
    st.set_page_config(layout="wide")
    st.title("The Seven Kingdoms")
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



