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
