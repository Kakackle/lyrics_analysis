from dash import Dash, html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc

import plotly.express as px
import plotly.graph_objects as graph_objects

from dataframes import (
    artist_freq_dist_df, genre_freq_dist_df,
    artists, genres
)

import ast
from itertools import islice

def take(n, iterable):
    """Return the first n items of the iterable as a list."""
    return list(islice(iterable, n))

# ---------------------------------------------------------------------------- #
#       Find words that are common in artist / genre more than in others       #
# ---------------------------------------------------------------------------- #

# ========= by artist =========
artist_freq_dist_controls = dbc.Card(
    [
        html.Div(
            [
            dbc.Label("Artist"),
            dcc.Dropdown(options = artists,
                        value = ['Al Green',],
                        id='freq-dist-artist-selection',
                        multi=True)
            ]),
    ],
    body=True,
)

artist_freq_dist_container = dbc.Container([
    html.H2(children = 'Find words that are common to artist more than others',
             style={'textAlign': 'center'}),
    dbc.Row(
        [
            dbc.Col(artist_freq_dist_controls, md=4),
            dbc.Col(dcc.Graph(id='artist-freq-dist-graph-content'), md=8),
        ],
        align="center",
    ),
], fluid=True)

def get_artist_freq_dist_callbacks(app):
    @app.callback(
        [
            Output('artist-freq-dist-graph-content', 'figure'),
        ],
        [
            Input('freq-dist-artist-selection', 'value'),
        ]
    )
    def update_artist_freq_dist_graph(artists):
        artist_dist_fig = graph_objects.Figure()
        for artist in artists:
            artist_comp_dict = artist_freq_dist_df[
                artist_freq_dist_df['Artist'] == artist]['sorted_comparison_dict'].values[0]
            
            artist_comp_dict = ast.literal_eval(artist_comp_dict)
            artist_comp_dict_no_unique = {k: v for k,v in artist_comp_dict.items() if v != 1000}
            
            no_unique_20 = take(20, artist_comp_dict_no_unique.items())
            words = [word[0] for word in no_unique_20]
            counts = [word[1] for word in no_unique_20]
            
            artist_dist_fig.add_trace(graph_objects.Bar(x=words, y=counts, name=artist))
                                    
        return [artist_dist_fig,]
    

# ======== by genre =========
genre_freq_dist_controls = dbc.Card(
    [
        html.Div(
            [
            dbc.Label("Genre"),
            dcc.Dropdown(options = genres,
                        value = ['soul',],
                        id='freq-dist-genre-selection',
                        multi=True)
            ]),
    ],
    body=True,
)

genre_freq_dist_container = dbc.Container([
    html.H2(children = 'Find words that are common to genre more than others',
             style={'textAlign': 'center'}),
    dbc.Row(
        [
            dbc.Col(genre_freq_dist_controls, md=4),
            dbc.Col(dcc.Graph(id='genre-freq-dist-graph-content'), md=8),
        ],
        align="center",
    ),
], fluid=True)

def get_genre_freq_dist_callbacks(app):
    @app.callback(
        [
            Output('genre-freq-dist-graph-content', 'figure'),
            Output('genre-freq-dist-df-shape', 'children')
        ],
        [
            Input('freq-dist-genre-selection', 'value'),
        ]
    )
    def update_genre_freq_dist_graph(genres):
        genre_dist_fig = graph_objects.Figure()
        for genre in genres:
            genre_comp_dict = genre_freq_dist_df[
                genre_freq_dist_df['genre'] == genre]['sorted_comparison_dict'].values[0]
            genre_comp_dict = ast.literal_eval(genre_comp_dict)
            genre_comp_dict_no_unique = {k: v for k,v in genre_comp_dict.items() if v != 1000}
            no_unique_20 = take(20, genre_comp_dict_no_unique.items())
            words = [word[0] for word in no_unique_20]
            counts = [word[1] for word in no_unique_20]
            
            genre_dist_fig.add_trace(graph_objects.Bar(x=words, y=counts, name=genre))
                                    
        return [genre_dist_fig,]