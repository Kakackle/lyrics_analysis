from dash import Dash, html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc

import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as graph_objects

from skimage import io

artist_bar_topic_rap_img = io.imread('../results/topic_counts_by_artist_rap_example.PNG')
artist_bar_topic_rap_fig = px.imshow(artist_bar_topic_rap_img)

artist_bar_topic_pop_img = io.imread('../results/topic_counts_by_artist_pop_example.PNG')
artist_bar_topic_pop_fig = px.imshow(artist_bar_topic_pop_img)

artist_bar_topic_examples = dbc.Container([
    html.H2(children='some examples', id='artist-bar-topic-examples'),

    dbc.Row(
            [
                dbc.Col(
                    html.Div(
                        [
                            dcc.Graph(figure = artist_bar_topic_rap_fig),
                            html.P(children = "Example 1 - Nas seems to be a rather sad artist in his lyrics")
                        ]
                    ), md=6
                ),
                dbc.Col(
                    html.Div(
                        [
                            dcc.Graph(figure = artist_bar_topic_pop_fig),
                            html.P(children = "Example 2 - Aaliyah was very much about love, not unlike her genre peers though, \
                                   except for Olivia Rodgrigo and Taylor Swift, who tend to write about breakups")
                        ]
                    ), md=6
                )

            ],
            align='center'
        ),

])

examples_div = html.Div(
    [
        artist_bar_topic_examples,
    ],
    id='examples-div'
)

examples_md_1 = dcc.Markdown(
'''
    Additionally, as stated in the introduction, static example comparisons / observations were taken, to provide further insight / a proper, 
    non-interactive analysis.
'''
)
    