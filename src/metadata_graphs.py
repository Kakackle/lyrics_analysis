from dash import Dash, html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc

import plotly.express as px
import plotly.graph_objects as graph_objects
from plotly.subplots import make_subplots

from dataframes import (
    genre_mean_df, artist_mean_df,
    counts_df,
    meta_columns
)

# ---------------------------------------------------------------------------- #
#       Artist metadata (unique_words, producer_count etc) means by genre      #
# ---------------------------------------------------------------------------- #
genre_metadata_controls = dbc.Card(
    [
        html.Div(
            [
            dbc.Label("Metadata selection"),
            dcc.Dropdown(options = meta_columns,
                        value = 'unique_words',
                        id='genre-metadata-selection')
            ]),
    ],
    body=True,
)

genre_metadata_container = dbc.Container([
    html.H1(children = 'Artist metadata mean by genre comparison', style={'textAlign': 'center'}),
    html.P(id="genre-metadata-df-shape"),
    dbc.Row(
        [
            dbc.Col(genre_metadata_controls, md=4),
            dbc.Col(dcc.Graph(id='genre-metadata-graph-content'), md=8),
        ],
        align="center",
    ),
], fluid=True)

def get_genre_metadata_callbacks(app):
    @app.callback(
        [
            Output('genre-metadata-graph-content', 'figure'),
            Output('genre-metadata-df-shape', 'children')
        ],
        [
            Input('genre-metadata-selection', 'value'),
        ]
    )
    def update_genre_metadata_graph(meta_col):
        # meta_fig = px.bar(genre_mean_df, x=genre_mean_df.index, y=genre_mean_df[meta_col])
        meta_fig = px.bar(genre_mean_df, x=genre_mean_df.index, y=genre_mean_df[meta_col])
        # meta_fig = graph_objects.Figure()
        return meta_fig, f'chosen meta_col: {meta_col}, shape: {genre_mean_df[meta_col].shape}'
    
# ---------------------------------------------------------------------------- #
#       Artist metadata (unique_words, producer_count etc) means by artist      #
# ---------------------------------------------------------------------------- #
# artist_mean_df
artist_metadata_controls = dbc.Card(
    [
        html.Div(
            [
            dbc.Label("Metadata selection"),
            dcc.Dropdown(options = meta_columns,
                        value = 'unique_words',
                        id='artist-metadata-selection')
            ]),
    ],
    body=True,
)

artist_metadata_container = dbc.Container([
    html.H1(children = 'Artist metadata mean by artist comparison', style={'textAlign': 'center'}),
    html.P(id="artist-metadata-df-shape"),
    dbc.Row(
        [
            dbc.Col(artist_metadata_controls, md=4),
            dbc.Col(dcc.Graph(id='artist-metadata-graph-content'), md=8),
        ],
        align="center",
    ),
], fluid=True)

def get_artist_metadata_callbacks(app):
    @app.callback(
        [
            Output('artist-metadata-graph-content', 'figure'),
            Output('artist-metadata-df-shape', 'children')
        ],
        [
            Input('artist-metadata-selection', 'value'),
        ]
    )
    def update_artist_metadata_graph(meta_col):
        # meta_fig = px.bar(genre_mean_df, x=genre_mean_df.index, y=genre_mean_df[meta_col])
        meta_fig = px.bar(artist_mean_df, x=artist_mean_df['Artist'], y=artist_mean_df[meta_col])
        # meta_fig = graph_objects.Figure()
        return meta_fig, f'chosen meta_col: {meta_col}, shape: {artist_mean_df[meta_col].shape}'


# ---------------------------------------------------------------------------- #
#              Artist metadata means by year overlaid bar and line             #
# ---------------------------------------------------------------------------- #
by_year_df = counts_df.groupby(by=['Year'])
by_year_means = by_year_df[[*meta_columns]].mean()

bar_line_metadata_controls = dbc.Card(
    [
        html.Div(
            [
            dbc.Label("Bar metadata column"),
            dcc.Dropdown(options = meta_columns,
                        value = 'unique_words',
                        id='bar-metadata-selection')
            ]),
        html.Div(
            [
            dbc.Label("Line metadata column"),
            dcc.Dropdown(options = meta_columns,
                        value = 'writer_count',
                        id='line-metadata-selection')
            ]),
    ],
    body=True,
)

bar_line_metadata_container = dbc.Container([
    html.H1(children = 'Artist metadata bar and line overlaid by year', style={'textAlign': 'center'}),
    html.P(id="bar-line-metadata-df-shape"),
    dbc.Row(
        [
            dbc.Col(bar_line_metadata_controls, md=4),
            dbc.Col(dcc.Graph(id='bar-line-metadata-graph-content'), md=8),
        ],
        align="center",
    ),
], fluid=True)

def get_bar_line_metadata_callbacks(app):
    @app.callback(
        [
            Output('bar-line-metadata-graph-content', 'figure'),
            Output('bar-line-metadata-df-shape', 'children')
        ],
        [
            Input('bar-metadata-selection', 'value'),
            Input('line-metadata-selection', 'value'),
        ]
    )
    def update_bar_line_metadata_graph(bar_col, line_col):
        year_fig = make_subplots(specs=[[{"secondary_y": True}]])

        year_fig.add_trace(
        graph_objects.Bar(x=by_year_means.index, y=by_year_means[bar_col],
                            name=bar_col),
        secondary_y=False,
        )

        year_fig.add_trace(
        graph_objects.Scatter(x=by_year_means.index, y=by_year_means[line_col],
                                name=line_col),
        secondary_y=True,
        )

        year_fig.update_layout(
            title_text=f"{bar_col} and {line_col}"
        )
        # Set y-axes titles
        year_fig.update_yaxes(title_text=bar_col, secondary_y=False)
        year_fig.update_yaxes(title_text=line_col, secondary_y=True)
        
        return year_fig, f'chosen bar_col: {bar_col}, line_col: {line_col}'

