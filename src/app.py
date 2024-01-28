from dash import Dash, html, dcc, callback, Output, Input, dash_table
import dash_bootstrap_components as dbc

import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as graph_objects

import pandas as pd

from wordcloud import WordCloud


from dataframes import (
    counts_df, top_20_filtered_words_artist_df, top_20_filtered_words_genre_df,
    artist_ngrams_df, genre_ngrams_df, genre_mean_df, genre_sum_df,
    artist_mean_df, artist_sum_df, artist_freq_dist_df, genre_freq_dist_df,
    artist_sentiment_counts_df, genre_sentiment_counts_df,
    artists, topics,
)


# ---------------------------------------------------------------------------- #
#               import graph containers and callbacks from files               #
# ---------------------------------------------------------------------------- #

from topic_graphs import (
    topic_container, get_topic_callbacks,
    bar_topic_container, get_topic_bar_callbacks,
    artist_bar_topic_container, get_artist_bar_topic_callbacks,
    topic_scatter_container, get_topic_scatter_callbacks,
    )

from frequency_graphs import (
    artist_freq_dist_container, get_artist_freq_dist_callbacks,
    genre_freq_dist_container, get_genre_freq_dist_callbacks
)

from metadata_graphs import (
    genre_metadata_container, get_genre_metadata_callbacks,
    artist_metadata_container, get_artist_metadata_callbacks,
    bar_line_metadata_container, get_bar_line_metadata_callbacks
)

from static_graphs import (
    corr_container,
    topic_spine_container,
    genre_sentiment_spine_container,
    artist_sentiment_spine_container,
    genre_emotion_spine_container,
    genre_wordcloud_container
)

from artist_wordcloud_graphs import (
    artist_wordcloud_container, get_artist_wordcloud_callbacks
)

from ngram_wordcloud_graphs import (
    ngram_artist_wordcloud_container, get_ngram_artist_wordcloud_callbacks
)

from analysis_examples import (
    artist_bar_topic_examples, examples_div
)

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

server = app.server

# ---------------------------------------------------------------------------- #
#                                  callbacks                                  #
# ---------------------------------------------------------------------------- #

get_topic_callbacks(app)
get_topic_bar_callbacks(app)
get_artist_bar_topic_callbacks(app)
get_topic_scatter_callbacks(app)

get_artist_freq_dist_callbacks(app)
get_genre_freq_dist_callbacks(app)

get_genre_metadata_callbacks(app)
get_artist_metadata_callbacks(app)
get_bar_line_metadata_callbacks(app)

get_artist_wordcloud_callbacks(app)

get_ngram_artist_wordcloud_callbacks(app)


# ---------------------------------------------------------------------------- #
#                          sidebar with nav to content                         #
# ---------------------------------------------------------------------------- #

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
# eg. margin-left is 2rem bigger than sidebar width
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

# TODO: przydalby sie tu jakis dropdown dzielacy na kategorie
# a przede wszystkim dzielacy na czesc interaktywna oraz na statyczna, z wlasna dokonana analiza

interactive_graph_links = dbc.Nav([
    dbc.NavLink("topic-graph-content", href="#topic-graph-content",
                             external_link=True),
    dbc.NavLink("bar-topic-graph-content", href="#bar-topic-graph-content",
                    external_link=True),
    dbc.NavLink("artist-bar-topic-graph-content", href="#artist-bar-topic-graph-content",
                    external_link=True),
    dbc.NavLink("topic-scatter-graph-content", href="#topic-scatter-graph-content",
                    external_link=True),
    dbc.NavLink("artist-freq-dist-graph-content", href="#artist-freq-dist-graph-content",
                    external_link=True),
    dbc.NavLink("genre-freq-dist-graph-content", href="#genre-freq-dist-graph-content",
                    external_link=True),
    dbc.NavLink("genre-metadata-graph-content", href="#genre-metadata-graph-content",
                    external_link=True),
    dbc.NavLink("genre-metadata-graph-content", href="#genre-metadata-graph-content",
                    external_link=True),
    dbc.NavLink("artist-metadata-graph-content", href="#artist-metadata-graph-content",
                    external_link=True),
    dbc.NavLink("bar-line-metadata-graph-content", href="#bar-line-metadata-graph-content",
                    external_link=True),
    dbc.NavLink("corr-graph-content", href="#corr-graph-content",
                    external_link=True),
    dbc.NavLink("topic-spine-graph-content", href="#topic-spine-graph-content",
                    external_link=True),
    dbc.NavLink("genre-sentiment-spine-graph-content", href="#genre-sentiment-spine-graph-content",
                    external_link=True),
    dbc.NavLink("artist-sentiment-spine-graph-content", href="#artist-sentiment-spine-graph-content",
                    external_link=True),
    dbc.NavLink("genre-emotion-spine-graph-content", href="#genre-emotion-spine-graph-content",
                    external_link=True),
    dbc.NavLink("genre-wordcloud-graph-content", href="#genre-wordcloud-graph-content",
                    external_link=True),
    dbc.NavLink("artist-wordcloud-graph-content", href="#artist-wordcloud-graph-content",
                    external_link=True),
    dbc.NavLink("genre-wordcloud-graph-content", href="#genre-wordcloud-graph-content",
                    external_link=True),
    dbc.NavLink("ngram-artist-wordcloud-graph-content", href="#ngram-artist-wordcloud-graph-content",
                    external_link=True),
    ],
    vertical=True,
    pills=True,
)

topic_graph_links = dbc.Nav([
    dbc.NavLink("topic-graph-content", href="#topic-graph-content",
                             external_link=True),
    dbc.NavLink("bar-topic-graph-content", href="#bar-topic-graph-content",
                    external_link=True),
    dbc.NavLink("artist-bar-topic-graph-content", href="#artist-bar-topic-graph-content",
                    external_link=True),
    dbc.NavLink("topic-scatter-graph-content", href="#topic-scatter-graph-content",
                    external_link=True),
    ],
    vertical=True,
    pills=True,
)


static_graph_links = dbc.Nav([
    dbc.NavLink("examples-div", href="#examples-div",
                    external_link=True),
    ],
    vertical=True,
    pills=True,
)

sidebar_groups = html.Div(
    dbc.Accordion(
        [
            dbc.AccordionItem(
                [
                    dbc.NavLink("Home", href="#start", external_link=True),
                ],
                title="Home / Intro",
            ),
            dbc.AccordionItem(
                [
                    interactive_graph_links,
                ],
                title="Interactive charts",
            ),
            dbc.AccordionItem(
                [
                    static_graph_links,
                ],
                title="Static graph links",
            ),

            dbc.Accordion(
                [
                    dbc.AccordionItem(
                        [
                            topic_graph_links,
                        ],
                        title="Interactive topic graphs"
                    )
                ]
            )

        ],
    )
)


sidebar = html.Div(
    [
        html.H2("Sidebar", className="display-4"),
        html.Hr(),
        html.P(
            "A simple sidebar layout with navigation links for same page", 
            className="lead"
        ),
        sidebar_groups,
    ],
    style=SIDEBAR_STYLE,
)

# ---------------------------------------------------------------------------- #
#                       df table and extra markdown intro                      #
# ---------------------------------------------------------------------------- #

## table
df_table = dash_table.DataTable(
    counts_df.to_dict('records'),
    columns=[{"name": c, "id": c} for c in counts_df.columns],

    filter_action="native",
    sort_action="native",
    # sort_mode="multi",

    page_action="native",
    page_current= 0,
    page_size= 10,
    style_cell={'textAlign': 'left'},

    style_as_list_view=True,
    style_data={
        'color': 'black',
        'backgroundColor': 'white'
    },
    style_data_conditional=[
        {
            'if': {'row_index': 'odd'},
            'backgroundColor': 'rgb(220, 220, 220)',
        }
    ],
    style_header={
        'backgroundColor': 'rgb(210, 210, 210)',
        'color': 'black',
        'fontWeight': 'bold'
    },
    style_table={"overflowX": "auto"},
)


md_intro = dcc.Markdown(
'''
    Analyzing relationships between lyrics of selected 10 artists from selected 4 genres
    (pop, rap, rock and soul), the artists include:  

    TODO: tutaj jakas tablica z artystami i przynaleznoscia do gatunkow

    from whose discographies the lyrics to each artist's popular songs were taken from genius.com
    using an API wrapper by TODO: link do johnwmillr

    The main metric choice was personal taste, but also guided by popularity on
    artist releases on rateyourmusic.com

    With 20 songs, the analysis can at best be considered powierzchowna, ciekawostkowa, mimo to
    zaleznosci sa zauwazalne

    Potem cos o metodach typu o topics itd  

    * du
    * du 
    * du
'''
)

# ---------------------------------------------------------------------------- #
#                        app content layout                                    #
# ---------------------------------------------------------------------------- #

content_div = html.Div([
    html.H1(children='Lyrics analysis project', id='start'),
    md_intro,
    df_table,
    html.Hr(),
    topic_container, html.Hr(),
    bar_topic_container, html.Hr(),
    artist_bar_topic_container, html.Hr(),
    topic_scatter_container, html.Hr(),

    artist_freq_dist_container, html.Hr(),
    genre_freq_dist_container, html.Hr(),

    genre_metadata_container, html.Hr(),
    artist_metadata_container, html.Hr(),
    bar_line_metadata_container, html.Hr(),

    corr_container, html.Hr(),
    topic_spine_container, html.Hr(),
    genre_sentiment_spine_container, html.Hr(),
    artist_sentiment_spine_container, html.Hr(),
    genre_emotion_spine_container, html.Hr(),
    genre_wordcloud_container, html.Hr(),

    artist_wordcloud_container, html.Hr(),

    ngram_artist_wordcloud_container, html.Hr(),

    # artist_bar_topic_examples, html.Hr(),
    examples_div

], id='page-content', style=CONTENT_STYLE)

app.layout = html.Div([sidebar, content_div])

# app.run(debug=True)
if __name__ == '__main__':
    app.run_server(debug=False)