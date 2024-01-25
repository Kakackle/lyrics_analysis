from dash import Dash, html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc

from dataframes import (
    artist_freq_dist_df, genre_freq_dist_df,
    artists
)

import ast
from itertools import islice

def take(n, iterable):
    """Return the first n items of the iterable as a list."""
    return list(islice(iterable, n))

# ---------------------------------------------------------------------------- #
#       Find words that are common in artist / genre more than in others       #
# ---------------------------------------------------------------------------- #
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
    html.H1(children = 'Find words that are common to artist more than others', style={'textAlign': 'center'}),
    html.P(id="artist-freq-dist-df-shape"),
    dbc.Row(
        [
            dbc.Col(artist_freq_dist_controls, md=4),
            dbc.Col(dcc.Graph(id='artist-freq-dist-graph-content'), md=8),
        ],
        align="center",
    ),
], fluid=True)