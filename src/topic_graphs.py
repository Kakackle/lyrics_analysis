"""
Topic counts from selected artists by year
"""
from dash import Dash, html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as graph_objects

from dataframes import (counts_df, genre_sum_df,
                            artist_sum_df, topics, genres, artists)

# ---------------------------------------------------------------------------- #
#                  Topic counts from selected artists by year                 #
# ---------------------------------------------------------------------------- #
# controls
topic_controls = dbc.Card(
    [
        html.Div(
            [
            dbc.Label("Genre"),
            dcc.Dropdown(
                id='topic-genre-selection',
                value = ['soul'],
                options = genres,
                multi = True
            )
            ]),
        html.Div(
            [
            dbc.Label("Artist"),
            dcc.Dropdown(
                id='topic-artist-selection-dynamic',
                value=['Al Green'],
                multi = True
            )
            ]),
        html.Div(
            [
            dbc.Label("Manual word topic"),
            dcc.Dropdown(topics, 'manual_love_count',
                          id='topic-selection')
            ]),
    ],
    body=True,
)

# layout
topic_container = dbc.Container([
    html.H2(children = 'Genre and Artist manual topic counts by year',
             style={'textAlign': 'center'}),
    dbc.Row(
        [
            dbc.Col(topic_controls, md=4),
            dbc.Col(dcc.Graph(id='topic-graph-content'), md=8),
        ],
        align="center",
    ),
], fluid=True)

# callbacks
def get_topic_callbacks(app):
    # ======== graph ==========
    @app.callback(
        [
            Output('topic-graph-content', 'figure'),
        ],
        [
            Input('topic-genre-selection', 'value'),
            Input('topic-artist-selection-dynamic', 'value'),
            Input('topic-selection', 'value'),
        ]
    )
    def update_topic_graph(genres, artists, topic):
        genre_df = counts_df[counts_df['genre'].isin(genres)]
        # in case there is only one artist selected
        artists_list = [artist for artist in artists]
        artists_df = genre_df[genre_df['Artist'].isin(artists_list)]

        fig = px.bar(artists_df, x='Year', y=topic, color='genre',
                    hover_data = ['Artist'])
        
        return [fig,]

    # ========= set available artist options based on chosen genre =========
    @app.callback(
        Output('topic-artist-selection-dynamic', 'options'),
        Input('topic-genre-selection', 'value')
    )
    def set_dynamic_artist_options(genres):
        options = dict()
        for genre in genres:
            genre_artists = list(counts_df[counts_df['genre'] == genre]['Artist'].unique())
            for artist in genre_artists:
                options[artist] = artist
        return options

    # ======= choose from available dynamic options =========
    # has to be done manually due to dynamicity
    # also this is how to return multiple options
    # in case of one you'd have to take [0] of value from options
    @app.callback(
        Output('topic-artist-selection-dynamic', 'value'),
        Input('topic-artist-selection-dynamic', 'options')
    )
    def set_dynamic_artist_value(options):
        # output = [option for option in options]
        # return output
        return options


# ---------------------------------------------------------------------------- #
#              Topic counts /percentages comparison by genre bars              #
# ---------------------------------------------------------------------------- #
# controls
bar_topic_controls = dbc.Card(
    [
        html.Div(
            [
            dbc.Label("Manual word topic"),
            dcc.Dropdown(options = topics,
                        value = ['manual_love_count',],
                        id='bar-topic-selection',
                        multi=True)
            ]),
    ],
    body=True,
)

# layout
bar_topic_container = dbc.Container([
    html.H2(children = 'Genre topic bars comparison', 
            style={'textAlign': 'center'}),
    dbc.Row(
        [
            dbc.Col(bar_topic_controls, md=4),
            dbc.Col(dcc.Graph(id='bar-topic-graph-content'), md=8),
        ],
        align="center",
    ),
], fluid=True)

# Topic bar callbacks
def get_topic_bar_callbacks(app):
    @app.callback(
        [
            Output('bar-topic-graph-content', 'figure'),
        ],
        [
            Input('bar-topic-selection', 'value'),
        ]
    )
    def update_bar_topic_graph(topics):
        bar_fig = graph_objects.Figure()
        # in case there is only one selected topic - turn input into a list:
        topics_list = [topic for topic in topics]
        for topic in topics_list:
            bar_fig.add_trace(graph_objects.Bar(y=genre_sum_df[topic].values,
                                                 x=genre_sum_df.index,
                                                   name=topic))
        
        return [bar_fig,]
    

# ---------------------------------------------------------------------------- #
#      Topic counts /percentages comparison by artist bars (within genre)      #
# ---------------------------------------------------------------------------- #

artist_bar_topic_controls = dbc.Card(
    [
        html.Div(
            [
            dbc.Label("Manual word topic"),
            dcc.Dropdown(options = topics,
                        value = ['manual_love_count',],
                        id='artist-bar-topic-selection',
                        multi=True)
            ]),
        html.Div(
            [
            dbc.Label("Genre"),
            dcc.Dropdown(options = list(genres),
                        value = ['pop',],
                        id='artist-bar-genre-selection')
            ]),
    ],
    body=True,
)

artist_bar_topic_container = dbc.Container([
    html.H2(children = 'Within genre artists topic bars comparison',
             style={'textAlign': 'center'}),
    dbc.Row(
        [
            dbc.Col(artist_bar_topic_controls, md=4),
            dbc.Col(dcc.Graph(id='artist-bar-topic-graph-content'), md=8),
        ],
        align="center",
    ),
], fluid=True)

def get_artist_bar_topic_callbacks(app):
    # Topic counts /percentages comparison by artist bars (within genre)
    @app.callback(
        [
            Output('artist-bar-topic-graph-content', 'figure'),
        ],
        [
            Input('artist-bar-topic-selection', 'value'),
            Input('artist-bar-genre-selection', 'value'),
        ]
    )
    def update_artist_bar_topic_graph(topics, genre):
        bar_fig = graph_objects.Figure()
        genre_df = artist_sum_df[artist_sum_df['genre'] == genre]
        genre_artists = list(genre_df['Artist'].unique())
        # in case there is only one selected topic - turn input into a list:
        topics_list = [topic for topic in topics]
        for topic in topics_list:
            bar_fig.add_trace(graph_objects.Bar(y=genre_df[topic].values,
                                                 x=genre_artists, name=topic))
        
        return [bar_fig,]


# ---------------------------------------------------------------------------- #
#       scatter for artist / genre where x = one topic, y = second topic       #
# ---------------------------------------------------------------------------- #
# colored by gender or genre
topic_scatter_controls = dbc.Card(
    [
        html.Div(
            [
            dbc.Label("Manual word topic (Y)"),
            dcc.Dropdown(options = topics,
                        value = 'manual_joy_count',
                        id='scatter-topic-Y-selection')
            ]),
        html.Div(
            [
            dbc.Label("Manual word topic (X)"),
            dcc.Dropdown(options = topics,
                        value = 'manual_sadness_count',
                        id='scatter-topic-X-selection')
            ]),
        html.Div(
            [
            dbc.Label("color by"),
            dcc.Dropdown(options = ['genre', 'gender'],
                        value = 'genre',
                        id='topic-scatter-color-selection')
            ]),
    ],
    body=True,
)

topic_scatter_container = dbc.Container([
    html.H2(children = 'scatter for all artists where x = one topic, \
             y = second topic', style={'textAlign': 'center'}),
    dbc.Row(
        [
            dbc.Col(topic_scatter_controls, md=4),
            dbc.Col(dcc.Graph(id='topic-scatter-graph-content'), md=8),
        ],
        align="center",
    ),
], fluid=True)

def get_topic_scatter_callbacks(app):
    # scatter for artist / genre where x = one topic, y = second topic
    @app.callback(
        [
            Output('topic-scatter-graph-content', 'figure'),
        ],
        [
            Input('scatter-topic-Y-selection', 'value'),
            Input('scatter-topic-X-selection', 'value'),
            Input('topic-scatter-color-selection', 'value'),
        ]
    )
    def update_artist_bar_topic_graph(topic_X, topic_Y, colorby):
        scatter_fig = px.scatter(artist_sum_df, x=topic_X, y=topic_Y,
                                    color=colorby)
        # return scatter_fig, f'topic_X: {topic_X}, topic_Y: {topic_Y}, colorby: {colorby}'
        return [scatter_fig,]


