import altair as alt

custom_palette = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf',
                  '#aec7e8', '#ffbb78', '#98df8a', '#ff9896', '#c5b0d5', '#c49c94', '#f7b6d2', '#c7c7c7', '#dbdb8d', '#9edae5',
                  '#393b79', '#7b4173', '#ff0000', '#0000ff', '#00ff00', '#ffff00', '#ff00ff', '#00ffff', '#800000', '#008000',
                  '#000080', '#800080', '#008080', '#808000', '#ff4500', '#228b22', '#0000cd', '#ffc0cb', '#dda0dd', '#b0c4de',
                  '#ffffe0', '#f0fff0', '#f0f8ff', '#f5f5f5', '#faebd7', '#7fffd4', '#f0ffff', '#f5deb3', '#adff2f', '#ff6347',
                  '#ffe4e1', '#da70d6', '#d3d3d3', '#90ee90', '#ff00ff', '#ffd700', '#a52a2a', '#20b2aa', '#778899', '#b0e0e6',
                  '#800080', '#a9a9a9', '#000000', '#006400', '#f08080', '#808080', '#add8e6', '#f08080', '#008000', '#ffdab9',
                  '#d3d3d3', '#ff0000', '#daa520', '#808080', '#c0c0c0', '#800000', '#ffff00', '#90ee90', '#ffd700', '#d2b48c',
                  '#f5f5f5', '#ffa500', '#ffdab9', '#d3d3d3', '#8b4513', '#ffffff', '#c0c0c0', '#ff00ff', '#800000', '#808000',
                  '#ffa500', '#ffff00', '#008000', '#00ff00', '#000080', '#008080', '#0000ff', '#00ffff', '#800080', '#ff0000',
                  '#ff00ff', '#008080', '#00ff00', '#000080', '#008080', '#0000ff', '#00ffff', '#800080', '#ff0000', '#ff00ff',
                  '#008080', '#00ff00', '#000080', '#008080', '#0000ff', '#00ffff', '#800080', '#ff0000', '#ff00ff', '#008080',
                  '#00ff00', '#000080', '#008080', '#0000ff', '#00ffff', '#800080', '#ff0000', '#ff00ff', '#008080', '#00ff00',
                  '#000080', '#008080', '#0000ff', '#00ffff', '#800080', '#ff0000', '#ff00ff', '#008080', '#00ff00', '#000080',
                  '#008080', '#0000ff', '#00ffff', '#800080']

def plotKillerMethod(df, killer_type):
    # Calcular o número de mortes por casa e método
    death_counts = df.groupby([killer_type, 'method']).size().reset_index(name='count')
    if killer_type == 'killer':
        titulo = "Assassino"
    else:
        titulo = "Aliança do Assassino"

    # Ordenar os dados pelo número de mortes
    death_counts_sorted = death_counts.sort_values(by='count', ascending=False)

    chart = alt.Chart(death_counts_sorted).mark_bar().encode(
        x=alt.X('count:Q', stack='normalize', axis=alt.Axis(title='Proporção')),
        y=alt.Y(f'{killer_type}:N', sort='-x', axis=alt.Axis(title=titulo)),
        # color=alt.Color('method:N', scale=alt.Scale(scheme=color_scheme)),
        color=alt.Color('method:N', scale=alt.Scale(range=custom_palette)),
        tooltip=['method', 'count']
    ).properties(
        width=600,
        height = 650,
        title=f'Causador da Morte ({killer_type}) e método (Ordenado por Número de Execuções)'
    )

    # Exibir o gráfico
    return chart

def deathsByAllegiance(df):
    # Calcular a contagem de alianças por temporada
    counts = df.groupby(['season', 'allegiance']).size().reset_index(name='count')

    # Criar o gráfico de barras empilhadas horizontal com interatividade
    bars = alt.Chart(counts).mark_bar().encode(
        y=alt.Y('season:N', axis=alt.Axis(title='Temporada')),
        x=alt.X('sum(count):Q', axis=alt.Axis(title='Quantidade de Baixas por Alianças')),
        color=alt.Color('allegiance:N', legend=alt.Legend(title='Aliança')),
        tooltip=['season:N', 'allegiance:N', 'count:Q'],
        # row='name:N'
    ).properties(
        width=1000,
        height=650,
        title='Quantidade de Execuções Facção/Temporada'
    ).interactive()

    # Exibir o gráfico
    return bars

def deathsByCharacter(df):
    # Calcular a contagem de alianças por temporada
    counts = df.groupby(['killer', 'method']).size().reset_index(name='count')

    # Ordenar os dados pelo número de ocorrências no eixo x
    counts_sorted = counts.sort_values(by='count', ascending=False)

    # Limitar aos 10 mais frequentes
    counts_top10 = counts_sorted.head(10)

    # Criar o gráfico de barras empilhadas horizontal com interatividade
    bars = alt.Chart(counts_sorted).mark_bar().encode(
        y=alt.Y('killer:N', axis=alt.Axis(title='Personagem')),
        x=alt.X('count:Q', axis=alt.Axis(title='Quantidade de Baixas por Alianças')),
        color=alt.Color('method:N', legend=alt.Legend(title='Método')),
        tooltip=['killer:N', 'method:N', 'count:Q']
    ).properties(
        width=1000,
        height=600,
        title='Top 10 Personagens com Mais Execuções por Método'
    ).interactive()

    # Exibir o gráfico
    return bars

def plotScatterKill(df,width=1000,height=1000):
    # Calcular o número de assassinatos por combinação de 'killer', 'method' e 'location'
    counts = df.groupby(['name', 'killer', 'method', 'location']).size().reset_index(name='count')

    # Determinar o tamanho máximo e mínimo de contagem
    max_count = counts['count'].max()
    min_count = counts['count'].min()

    # Definir limites da escala de tamanho
    min_size = 50  # Tamanho mínimo
    max_size = 200  # Tamanho máximo

    # Criar o gráfico de dispersão com escala ajustada
    scatter = alt.Chart(counts).mark_circle().encode(
        x=alt.X('killer:N', axis=alt.Axis(title='Assassino')),
        y=alt.Y('name:N', axis=alt.Axis(title='Vítima')),
        color='location:N',
        size=alt.Size('count:Q',
                      scale=alt.Scale(domain=[min_count, max_count], range=[min_size, max_size]),
                      legend=alt.Legend(title='Contagem')),
        tooltip=['name', 'killer', 'method', 'location', 'count']
    ).properties(
        width=width,
        height=height,
        title='Relação entre Vítima, Assassino, Método e Localização'
    ).configure_axis(
        grid=True
    ).interactive()

    # Exibir o gráfico
    return scatter

# def get_new_df(lista_condicoes,df=deaths_df):
#     for condicao in lista_condicoes:
        