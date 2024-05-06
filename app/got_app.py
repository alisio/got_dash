import os
import requests
import streamlit as st
import pandas as pd
import altair as alt
import got_lib
from got_lib import plotKillerMethod,deathsByAllegiance,plotScatterKill,deathsByCharacter,escala_numero
import sys
# import seaborn as sns

deaths_df = pd.read_csv('./data/deaths.csv')

# Constantes
principais_personagens = [
    'Arya Stark', 'Cersei Lannister', 'Jon Snow', 'Olenna Tyrell', 'Sansa Stark', 'Tyrion Lannister', 'Bran Stark', 'Daenerys Targaryen', 'Jorah Mormont', 'Robb Stark', 'The High Sparrow', 'Catelyn Stark', 'Jaime Lannister', 'Littlefinger', 'Samwell Tarly', 'The Hound'
]
principais_personagens.sort()

principais_casas = [
    'House Stark', 'House Lannister', 'House Tyrell', 'House Targaryen', 'House Martell'
]
principais_personagens.sort()

top_executores = deaths_df['killer'].value_counts().reset_index()
top_executores.columns = ["Executor","Contagem"]


# Nesse dataset temos os nome de quem morreu, sua família/facção, a temporada, o número do episódio, o assassino, a família/facção do assassino, o método do assassinato e a contagem ordenada da morte. Vemos que alguns valoers não estão definidos, vamos resolver isso substituindo NaN por string vazia.

deaths_df = deaths_df.fillna('')

# %%


def pag_dados():
    # st.title("Dados")
    # Add code for rendering data and interactivity specific to Page 1
    # deaths_df
    tabbed_pages = st.tabs(["Indivíduo", "Aliança"])

    with tabbed_pages[0]:
        import exec_nome
        del sys.modules['exec_nome']

    with tabbed_pages[1]:
        import exec_casa
        del sys.modules['exec_casa']


def pag_execucoes():
    texto_sidebar = """
        # Descrição
        Esta página tem o objetivo de responder a perguntas relacionadas ao número de execuções causadas por alianças ou indivíduos, o método de execução utilizado, e o relacionamento entre executores, vítimas e locais de execução em Game of Thrones. As questões específicas que podem ser respondidas incluem:

        * Qual aliança ou indivíduo foi responsável pelo maior número de execuções?
        * Qual foi o método de execução preferido por Ramsay Bolton?
        * Quem executou Tywin Lannister, onde e como?
    
        """
    st.sidebar.image('./img/alisiomeneses_an_image_conveying_an_execution_in_westeros_feabeb8b-eec4-4de7-a50b-4c19f9c977ac.png')
    st.sidebar.write(texto_sidebar)
    st.title("Execuções:")
    # # Qual a casa/facção que mais causou mortes?
    # tipo_execucao = st.selectbox("Execução por: ", ['Indivíduo','Casa'])

    aba_exec_casa,aba_exec_individuo,aba_exec_relacionamento = st.tabs(["Aliança","Individuo","Relacionamento"])
    with aba_exec_casa:
        lista_casas = list(deaths_df["killers_house"].unique())
        casas_selecionadas = st.multiselect('Selecione as Alianças:',lista_casas,principais_casas)
        opcao = 'killers_house'
        df_tmp = deaths_df[deaths_df['killers_house'].isin(casas_selecionadas)]
        if len(df_tmp) == 0:
            # se nenhum item selecionado, exibe todos
            st.altair_chart(plotKillerMethod(deaths_df, opcao), use_container_width=True, theme="streamlit")
        else:
            st.altair_chart(plotKillerMethod(df_tmp, opcao), use_container_width=True, theme="streamlit")
    with aba_exec_individuo:
        opcao = 'killer'
        lista_executores = list(deaths_df["killer"].unique())
        lista_executores.sort()
        lista_top_5_executores = list(top_executores['Executor'][:5])
        executores_selecionados = st.multiselect('Selecione os Executores:',lista_executores,lista_top_5_executores)
        df_tmp = deaths_df[deaths_df["killer"].isin(executores_selecionados)]
        if len(df_tmp) == 0:
            st.altair_chart(plotKillerMethod(deaths_df, opcao,), use_container_width=True, theme="streamlit")
        else:
            st.altair_chart(plotKillerMethod(df_tmp, opcao,), use_container_width=True, theme="streamlit")
    with aba_exec_relacionamento:
        df_tmp = deaths_df.copy()
        num_executores = len(deaths_df.killer.unique())
        lista_vitimas = list(df_tmp['name'].unique())
        lista_executores = list(df_tmp['killer'].unique())
        lista_locais = list(df_tmp['location'].unique())
        lista_metodos = list(df_tmp['method'].unique())
        def atualiza_df():
            lista_vitimas = list(df_tmp['name'].unique())
            lista_executores = list(df_tmp['killer'].unique())
            lista_locais = list(df_tmp['location'].unique())
            lista_metodos = list(df_tmp['method'].unique())
        
        atualiza_df()
            

        col1, col2 = st.columns(2)
        
        # Assign each Streamlit object to a separate column
        with col1:
            vitimas_selecionadas = st.multiselect('Seleção de Vítimas', lista_vitimas)
            col_exec_1,col_exec_2 = st.columns(2)
            with col_exec_2:
                toggle_top_5_executores = st.toggle("Top 5 executores",value=True)
                if toggle_top_5_executores:
                    with col_exec_1:
                        executores_selecionados = st.multiselect('Seleção de Executores', lista_executores,lista_top_5_executores)
                else:
                    with col_exec_1:
                        executores_selecionados = st.multiselect('Seleção de Executores', lista_executores)
        with col2:
            locais_selecionados = st.multiselect('Seleção de Locais', lista_locais)
            metodos_selecionados = st.multiselect('Seleção de Métodos', lista_metodos)
        
        if len(vitimas_selecionadas) == 0:
            vitimas_selecionadas = lista_vitimas
        if len(executores_selecionados) == 0:
            executores_selecionados = lista_executores
        if len(locais_selecionados) == 0:
            locais_selecionados = lista_locais
        if len(metodos_selecionados) == 0:
            metodos_selecionados = lista_metodos

        condicao_1 = (df_tmp['killer'].isin(executores_selecionados))
        condicao_2 = (df_tmp['name'].isin(vitimas_selecionadas))
        condicao_3 = (df_tmp['location'].isin(locais_selecionados))
        condicao_4 = (df_tmp['method'].isin(metodos_selecionados))

        df_tmp = df_tmp[condicao_1 & condicao_2 & condicao_3 & condicao_4]
        # Utilizar o numero de executores para definir tamanho do scatterplot dinamicamente
        num_executores_base_selecionada = len(df_tmp.killer.unique())
        if len(df_tmp) == 0:
            st.markdown("Nenhum registro encontrado")
        else:
            st.altair_chart(plotScatterKill(df_tmp,height=escala_numero(num_executores_base_selecionada,1,num_executores)), use_container_width=False, theme="streamlit")

def pag_alianças():
    aba_alianca_casa,aba_alianca_individuo = st.tabs(["Aliança","Individuo"])
    texto_sidebar = """
        # Descrição
        Esta página tem o objetivo de responder a perguntas relacionadas ao número de baixas causadas por alianças ou indivíduos, por temporada e método de execução. As questões específicas podem incluir:
        * Qual aliança sofreu o maior número de baixas?
        * Em qual temporada ocorreram o maior número de baixas?
        * Qual foi o método de execução mais utilizado por um determinado personagem?
    
        """
    st.sidebar.image('./img/allegiances.webp')
    st.sidebar.write(texto_sidebar)
    with aba_alianca_casa:
        lista_casas = list(deaths_df["killers_house"].unique())
        casas_selecionadas = st.multiselect('Selecione as Alianças:',lista_casas,principais_casas)
        if len(casas_selecionadas) == 0:
            df_tmp = deaths_df
        else: 
            df_tmp = deaths_df[deaths_df['killers_house'].isin(casas_selecionadas)]

        st.altair_chart(deathsByAllegiance(df_tmp), use_container_width=False, theme="streamlit")
    with aba_alianca_individuo:
        lista_executores = list(deaths_df["killer"].unique())
        lista_executores.sort()
        lista_top_10_executores = list(top_executores['Executor'][:10])
        lista_metodos = list(deaths_df[deaths_df.killer.isin(lista_top_10_executores)]["method"].unique())
        df_tmp = deaths_df[deaths_df.killer.isin(lista_top_10_executores)].copy()
        col_allegiance_1,col_allegiance_2 = st.columns(2)

        with col_allegiance_1:
            executores_selecionados = st.multiselect('Selecione os Executores:',lista_top_10_executores)

        with col_allegiance_2:
            metodos_selecionados = st.multiselect('Selecione os Métodos:',lista_metodos)
        
        if len(metodos_selecionados) == 0:
            metodos_selecionados = lista_metodos
        if len(executores_selecionados) == 0:
            executores_selecionados = lista_top_10_executores
        
        condicao1 = (df_tmp['killer'].isin(executores_selecionados))
        condicao2 = (df_tmp['method'].isin(metodos_selecionados))
        df_tmp = df_tmp[condicao1 & condicao2]
        st.altair_chart(deathsByCharacter(df_tmp))
            
def pag_sobre():
    texto = """

    Para entusiastas de Game of Thrones e desenvolvedores Python. Este dashboard fornece uma interface interativa e fácil de usar para explorar e analisar um conjunto de dados abrangente contendo informações sobre personagens, casas, livros e temporadas.
    
    Este painel é um aplicativo web desenvolvido como trabalho do Curso de Especialização em Ciência de Dados, disciplina CD008 - Visualização de dados - Turma 3. Professor responsável: João Luiz Dihl Comba.

    Equipe:
    * Antonio Alisio de Meneses Cordeiro
    * Jeferson Jose de Miranda
    * Salvador Vicente Grisolia

    ## Código fonte:
    https://github.com/alisio/got_dash

    ## Reconhecimentos:
    * [Game of Thrones Datasets and Visualizations](https://github.com/jeffreylancaster/game-of-thrones)
    * Wikipedia (imagens dos personagens)
    * Midjourney (imagens dos personagens)
    """
    st.write(texto)

def app():
    st.set_page_config(layout="wide")
    st.title("The Seven Kingdoms")
    # Set up sidebar menu
    sidebar = st.sidebar
    selected_page = sidebar.selectbox("Selecione Uma Página", ["Resumo", "Execuções","Alianças","Sobre"])

    if selected_page == "Resumo":
        pag_dados()
    if selected_page == "Execuções":
        pag_execucoes()
    elif selected_page == "Alianças":
        pag_alianças()
    elif selected_page == "Sobre":
        pag_sobre()

app()



background_image = """
<style>
[data-testid="stAppViewContainer"] > .main {
    background-image: url('https://alisio.com.br/misc/images/midjourney_A_close_up_of_the_Iron_Throne_from_Game_of_Throne_75027b81-673f-45e0-8608-bced4d84031f.png');
    background-size: 100vw 100vh;  # This sets the size to cover 100% of the viewport width and height
    background-position: center;  
    background-repeat: no-repeat;
    
}
</style>
"""

st.markdown(background_image, unsafe_allow_html=True)