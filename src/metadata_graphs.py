from dash import Dash, html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc

import plotly.express as px
import plotly.graph_objects as graph_objects
from plotly.subplots import make_subplots

from dataframes import (
    genre_mean_df, artist_mean_df,
    counts_df,
    meta_columns,
    topics
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
    html.H3(children = 'Artist metadata by genre (mean)', style={'textAlign': 'center'}),
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
        ],
        [
            Input('genre-metadata-selection', 'value'),
        ]
    )
    def update_genre_metadata_graph(meta_col):
        # meta_fig = px.bar(genre_mean_df, x=genre_mean_df.index, y=genre_mean_df[meta_col])
        meta_fig = px.bar(genre_mean_df, x=genre_mean_df.index, y=genre_mean_df[meta_col])
        # meta_fig = graph_objects.Figure()
        return [meta_fig,]
    
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
    html.H3(children = 'Artist metadata by artist (mean)', style={'textAlign': 'center'}),
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
        ],
        [
            Input('artist-metadata-selection', 'value'),
        ]
    )
    def update_artist_metadata_graph(meta_col):
        # meta_fig = px.bar(genre_mean_df, x=genre_mean_df.index, y=genre_mean_df[meta_col])
        meta_fig = px.bar(artist_mean_df, x=artist_mean_df['Artist'], y=artist_mean_df[meta_col])
        # meta_fig = graph_objects.Figure()
        return [meta_fig,]


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
    html.H3(children = 'Artist metadata bar and line overlaid by year', style={'textAlign': 'center'}),
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
        
        return [year_fig,]
    
# ---------------------------------------------------------------------------- #
#                    genre bar line metadata vs topics                         #
# ---------------------------------------------------------------------------- #
    
bar_line_metadata_topic_controls = dbc.Card(
    [
        html.Div(
            [
            dbc.Label("Bar topic column"),
            dcc.Dropdown(options = topics,
                        value = 'manual_love_count',
                        id='bar-metadata-topic-topic-selection')
            ]),
        html.Div(
            [
            dbc.Label("Line metadata column"),
            dcc.Dropdown(options = meta_columns,
                        value = 'writer_count',
                        id='line-metadata-topic-meta-selection')
            ]),
    ],
    body=True,
)

bar_line_metadata_topic_container = dbc.Container([
    html.H3(children = 'Genre metadata vs topical mentions', style={'textAlign': 'center'}),
    dbc.Row(
        [
            dbc.Col(bar_line_metadata_topic_controls, md=4),
            dbc.Col(dcc.Graph(id='bar-line-metadata-topic-graph-content'), md=8),
        ],
        align="center",
    ),
], fluid=True)

def get_bar_line_metadata_topic_callbacks(app):
    @app.callback(
        [
            Output('bar-line-metadata-topic-graph-content', 'figure'),
        ],
        [
            Input('bar-metadata-topic-topic-selection', 'value'),
            Input('line-metadata-topic-meta-selection', 'value'),
        ]
    )
    def update_bar_line_metadata_topic_graph(bar_col, line_col):
        bl_fig = make_subplots(specs=[[{"secondary_y": True}]])

        bl_fig.add_trace(
        graph_objects.Bar(x=genre_mean_df.index, y=genre_mean_df[bar_col],
                            name=bar_col),
        secondary_y=False,
        )

        bl_fig.add_trace(
        graph_objects.Scatter(x=genre_mean_df.index, y=genre_mean_df[line_col],
                                name=line_col),
        secondary_y=True,
        )

        bl_fig.update_layout(
            title_text=f"{bar_col} and {line_col}"
        )
        # Set y-axes titles
        bl_fig.update_yaxes(title_text=bar_col, secondary_y=False)
        bl_fig.update_yaxes(title_text=line_col, secondary_y=True)
        
        return [bl_fig,]

    
meta_md_1 = dcc.Markdown(
'''
    Additionally, other potential differentiating factors, not directly related to lyrics were explored.
    These factors include artist metadata such as featured artist, producer and writer counts for songs, the 
    and the vocabulary sizes.

    These visualizations are meant to look for potential correlations between them both between genres and artists,
    which may help add some context or potential causes to differences observed from previous parts.
     
'''
)

