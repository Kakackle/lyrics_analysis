from dash import Dash, html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc

import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as graph_objects

from wordcloud import WordCloud

from dataframes import (
    top_20_filtered_words_artist_df,
    genres,
    count_cols, word_cols
)

artist_wordcloud_controls = dbc.Card(
    [
        html.Div(
            [
            dbc.Label("Genre"),
            dcc.Dropdown(
                id='wordcloud-genre-selection',
                value = 'soul',
                options = list(top_20_filtered_words_artist_df.genre.unique())
            )
            ]),
        html.Div(
            [
            dbc.Label("Artist"),
            # dcc.Dropdown(df.Artist.unique(), 'Al Green', id='topic-artist-selection')
            dcc.Dropdown(
                id='wordcloud-artist-selection-dynamic',
                value='Al Green'
            )
            ]),
    ],
    body=True,
)

artist_wordcloud_container = dbc.Container([
    html.H2(children = 'Genre and Artist top words wordcloud dynamic', style={'textAlign': 'center'}),
    dbc.Row(
        [
            dbc.Col(artist_wordcloud_controls, md=4),
            dbc.Col(dcc.Graph(id='artist-wordcloud-graph-content'), md=8),
        ],
        align="center",
    ),
    # dbc.DropdownMenu(label="Artist", id="artist-selection", children=items),
    # dbc.Select(id="artist-selection", options=items),

], fluid=True)

def get_artist_wordcloud_callbacks(app):
    @app.callback(
        [
            Output('artist-wordcloud-graph-content', 'figure'),
        ],
        [
            Input('wordcloud-genre-selection', 'value'),
            Input('wordcloud-artist-selection-dynamic', 'value'),
        ]
    )
    def update_artist_wordcloud_graph(genre, artist):
        artist_df = top_20_filtered_words_artist_df[top_20_filtered_words_artist_df['Artist'] == artist]
        # create wordcloud and bar graph
        artist_words = [artist_df[word].values[0] for word in word_cols]
        artist_counts = [artist_df[count].values[0] for count in count_cols]

        d = {}
        for word, count in zip(artist_words, artist_counts):
            d[word] = count

        wordcloud = WordCloud(background_color = "white", width=800, height=400)
        wordcloud.generate_from_frequencies(frequencies=d)

        artist_fig = make_subplots(rows=1, cols=2, subplot_titles = [f'{artist} wordcloud', f'{artist} bar'])

        artist_fig.add_trace(graph_objects.Image(z=wordcloud), row = 1, col = 1)
        artist_fig.add_trace(graph_objects.Bar(x=artist_words, y=artist_counts, showlegend = False), row=1, col=2,)
        artist_fig.update_layout(height = 1 * 400)

        return [artist_fig,]

    # ========= set available artist options based on chosen genre =========
    @app.callback(
        Output('wordcloud-artist-selection-dynamic', 'options'),
        Input('wordcloud-genre-selection', 'value')
    )
    def set_dynamic_artist_options(genre):
        genre_artists = list(top_20_filtered_words_artist_df[top_20_filtered_words_artist_df['genre'] == genre]['Artist'].unique())
        options = [{"label": artist, "value": artist} for artist in genre_artists]
        return options

    # ======= choose from available dynamic options =========
    @app.callback(
        Output('wordcloud-artist-selection-dynamic', 'value'),
        Input('wordcloud-artist-selection-dynamic', 'options')
    )
    def set_dynamic_artist_value(options):
        return options[0]['value']