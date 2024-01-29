from dash import Dash, html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc

import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as graph_objects

from wordcloud import WordCloud

from dataframes import (
    artist_ngrams_df
)

# ---------------------------------------------------------------------------- #
#                          Dynamic artist ngram graph                          #
# ---------------------------------------------------------------------------- #

ngram_artist_wordcloud_controls = dbc.Card(
    [
        html.Div(
            [
            dbc.Label("Genre"),
            dcc.Dropdown(
                id='ngram-wordcloud-genre-selection',
                value = 'soul',
                options = list(artist_ngrams_df.genre.unique())
            )
            ]),
        html.Div(
            [
            dbc.Label("Artist"),
            dcc.Dropdown(
                id='ngram-wordcloud-artist-selection-dynamic',
                value='Al Green'
            )
            ]),
    ],
    body=True,
)

ngram_artist_wordcloud_container = dbc.Container([
    html.H2(children = 'Most common ngrams for artists and genres', style={'textAlign': 'center'}),
    html.P(id='ngram-wordcloud-df-shape'),
    dbc.Row(
        [
            dbc.Col(ngram_artist_wordcloud_controls, md=4),
            dbc.Col(dcc.Graph(id='ngram-artist-wordcloud-graph-content'), md=8),
        ],
        align="center",
    ),
], fluid=True)


def get_ngram_artist_wordcloud_callbacks(app):
    @app.callback(
        [
            Output('ngram-artist-wordcloud-graph-content', 'figure'),
        ],
        [
            Input('ngram-wordcloud-genre-selection', 'value'),
            Input('ngram-wordcloud-artist-selection-dynamic', 'value'),
        ]
    )
    def update_ngram_artist_wordcloud_graph(genre, artist):
        artist_df = artist_ngrams_df[artist_ngrams_df['Artist'] == artist]
        # create wordclouds for all ngram lens

        ngram_lens = [2,3,4]
        ngrams_n = 20
        n = len(ngram_lens) * ngrams_n

        gram_wordclouds_fig = make_subplots(rows=3, cols=2, subplot_titles = ngram_lens)

        for len_index, gram_len in enumerate(ngram_lens):
            gram_count_cols = []
            gram_cols = []
            for ind in range(ngrams_n):
                gram_cols.append(f'ngram_{gram_len}_{ind}')
                gram_count_cols.append(f'count_{gram_len}_{ind}')
                
            gram_words = [artist_df[word].values[0] for word in gram_cols]
            gram_counts = [artist_df[count].values[0] for count in gram_count_cols]
                
            d = {}
            for word, count in zip(gram_words, gram_counts):
                d[word] = count
                
            wordcloud = WordCloud(background_color = "white", width=800, height=400)
            wordcloud.generate_from_frequencies(frequencies=d)
            
            gram_wordclouds_fig.add_trace(graph_objects.Image(z=wordcloud), row=len_index+1, col=1)
            gram_wordclouds_fig.add_trace(graph_objects.Bar(x=gram_words, y=gram_counts, showlegend = False), row=len_index+1, col=2)
            
        gram_wordclouds_fig.update_layout(height = 3*400)
        # gram_wordclouds_fig.show()
        
        return [gram_wordclouds_fig,]

    # ========= set available artist options based on chosen genre =========
    @app.callback(
        Output('ngram-wordcloud-artist-selection-dynamic', 'options'),
        Input('ngram-wordcloud-genre-selection', 'value')
    )
    def set_ngram_dynamic_artist_options(genre):
        genre_artists = list(artist_ngrams_df[artist_ngrams_df['genre'] == genre]['Artist'].unique())
        options = [{"label": artist, "value": artist} for artist in genre_artists]
        return options

    # ======= choose from available dynamic options =========
    @app.callback(
        Output('ngram-wordcloud-artist-selection-dynamic', 'value'),
        Input('ngram-wordcloud-artist-selection-dynamic', 'options')
    )
    def set_ngram_dynamic_artist_value(options):
        return options[0]['value']
    
