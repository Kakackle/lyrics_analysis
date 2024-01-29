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
    topic_md_1
    )

from example_lyrics import (
    topic_max_md_1, topic_max_df_table
)

from frequency_graphs import (
    artist_freq_dist_container, get_artist_freq_dist_callbacks,
    genre_freq_dist_container, get_genre_freq_dist_callbacks,
    freq_md_1
)

from metadata_graphs import (
    genre_metadata_container, get_genre_metadata_callbacks,
    artist_metadata_container, get_artist_metadata_callbacks,
    bar_line_metadata_container, get_bar_line_metadata_callbacks,
    bar_line_metadata_topic_container, get_bar_line_metadata_topic_callbacks,
    meta_md_1
)

from static_graphs import (
    corr_container,
    topic_spine_container,
    genre_sentiment_spine_container,
    artist_sentiment_spine_container,
    genre_emotion_spine_container,
    genre_wordcloud_container,
    sentiment_md_1,
    corr_md_1,
    tsne_container,
)

from artist_wordcloud_graphs import (
    artist_wordcloud_container, get_artist_wordcloud_callbacks
)

from ngram_wordcloud_graphs import (
    ngram_artist_wordcloud_container, get_ngram_artist_wordcloud_callbacks
)

from analysis_examples import (
    artist_bar_topic_examples, examples_div,
    examples_md_1
)

from introduction import (
    md_intro_1, md_intro_2, md_intro_3,
    counts_df_table, artist_df_table
)

from about import (
    about_md_1
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
get_bar_line_metadata_topic_callbacks(app)

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

topic_graph_links = dbc.Nav([
    dbc.NavLink("Topic mentions by genre", href="#bar-topic-graph-content",
                    external_link=True),
    dbc.NavLink("Topic mentions by artist", href="#artist-bar-topic-graph-content",
                    external_link=True),
    dbc.NavLink("Relations between topic mentions", href="#topic-scatter-graph-content",
                    external_link=True),
    dbc.NavLink("Artist topic mentions by year", href="#topic-graph-content",
                    external_link=True),
    dbc.NavLink("Topic mentions comparison between male and female artist", href="#topic-spine-graph-content",
                    external_link=True),
    ],
    vertical=True,
    pills=True,
)

sentiment_graph_links = dbc.Nav([
    dbc.NavLink("Sentiment split between genres", href="#genre-sentiment-spine-graph-content",
                    external_link=True),
    dbc.NavLink("Sentiment split between artists", href="#artist-sentiment-spine-graph-content",
                    external_link=True),
    dbc.NavLink("Emotional split for genres", href="#genre-emotion-spine-graph-content",
                    external_link=True),
    ],
    vertical=True,
    pills=True,
)

word_graph_links = dbc.Nav([
    dbc.NavLink("Words more common to one artist than others", href="#artist-freq-dist-graph-content",
                    external_link=True),
    dbc.NavLink("Words more common to one genre than others", href="#genre-freq-dist-graph-content",
                    external_link=True),
    dbc.NavLink("Top 20 (filtered) words by genre WordCloud'", href="#genre-wordcloud-graph-content",
                    external_link=True),
    dbc.NavLink("Dynamic top words wordcloud", href="#artist-wordcloud-graph-content",
                    external_link=True),
    dbc.NavLink("Most common ngrams for artists and genres", href="#ngram-artist-wordcloud-graph-content",
                    external_link=True),
    ],
    vertical=True,
    pills=True,
)

meta_graph_links = dbc.Nav([
    dbc.NavLink("Artist metadata by genre (mean)", href="#genre-metadata-graph-content",
                    external_link=True),
    dbc.NavLink("Artist metadata by artist (mean)", href="#artist-metadata-graph-content",
                    external_link=True),
    dbc.NavLink("Artist metadata bar and line overlaid by year", href="#bar-line-metadata-graph-content",
                    external_link=True),
    dbc.NavLink("Genre metadata vs topical mentions", href="#bar-line-metadata-topic-graph-content",
                    external_link=True),
    ],
    vertical=True,
    pills=True,
)

corr_sne_graph_links = dbc.Nav([
    dbc.NavLink("Correlation Matrix", href="#corr-graph-content",
                    external_link=True),
    dbc.NavLink("t-SNE", href="#tsne-graph-content",
                    external_link=True),
    ],
    vertical=True,
    pills=True,
)


static_graph_links = dbc.Nav([
    dbc.NavLink("Examplary analysis", href="#examples-div",
                    external_link=True),
    ],
    vertical=True,
    pills=True,
)

introduction_links = dbc.Nav([
    dbc.NavLink("Home", href="#start", external_link=True),
    dbc.NavLink("Markdown Intro", href="#md-intro", external_link=True),
    dbc.NavLink("Counts df", href="#counts-df", external_link=True),
    ],
    vertical=True,
    pills=True,
)

extra_links = dbc.Nav([
    dbc.NavLink("About", href="#about-extra", external_link=True),
    ],
    vertical=True,
    pills=True,
)


sidebar_groups = html.Div(
    dbc.Accordion(
        [
            dbc.AccordionItem(
                [
                    introduction_links,
                ],
                title="Home / Introduction",
            ),

            dbc.AccordionItem(
                [
                    dbc.Accordion(
                        [
                        dbc.AccordionItem(
                                [
                                    topic_graph_links,
                                ],
                                title = 'Topic charts'
                            ),
                        dbc.AccordionItem(
                                [
                                    sentiment_graph_links,
                                ],
                                title = 'Sentiment charts'
                            ),  
                        dbc.AccordionItem(
                                [
                                    word_graph_links,
                                ],
                                title = 'Word charts'
                            ),  
                        dbc.AccordionItem(
                                [
                                    meta_graph_links,
                                ],
                                title = 'Meta charts'
                            ),  
                        dbc.AccordionItem(
                                [
                                    corr_sne_graph_links,
                                ],
                                title = 'Corr/sne charts'
                            ),  
                        ],
                    )
                ],
                title="Interactive charts",
            ),

            dbc.AccordionItem(
                [
                    static_graph_links,
                    extra_links,
                ],
                title="Static analysis",
            ),


        ],
    )
)


sidebar = html.Div(
    [
        html.H2("Lyrics analysis", className="display-4"),
        html.Hr(),
        html.P(
            "Navigate to sections of the analysis", 
            className="lead"
        ),
        sidebar_groups,
    ],
    style=SIDEBAR_STYLE,
)



# ---------------------------------------------------------------------------- #
#                        app content layout                                    #
# ---------------------------------------------------------------------------- #

intro_items = html.Div([
    html.H1(children='Lyrics analysis project', id='start'),
    md_intro_1,
    artist_df_table,
    md_intro_2,
    counts_df_table,
    md_intro_3
])

topic_charts = html.Div([
    html.H1(children='Topical analysis'),
    topic_md_1,
    bar_topic_container,
    artist_bar_topic_container, 
    topic_scatter_container, 
    topic_container,
    topic_spine_container,
    topic_max_md_1,
    topic_max_df_table
])

sentiment_charts = html.Div([
    html.H1(children='Sentiment / emotion analysis'),
    sentiment_md_1,
    genre_sentiment_spine_container,
    artist_sentiment_spine_container,
    genre_emotion_spine_container,
])

words_charts = html.Div([
    html.H1('Word-by-word analysis'),
    freq_md_1,
    artist_freq_dist_container,
    genre_freq_dist_container,
    genre_wordcloud_container,
    artist_wordcloud_container,
    ngram_artist_wordcloud_container,
])

meta_charts = html.Div([
    html.H1('Song metadata analysis'),
    meta_md_1,
    genre_metadata_container,
    artist_metadata_container,
    bar_line_metadata_container,
    bar_line_metadata_topic_container,
])

corr_sne_charts = html.Div([
    html.H1('Correlations'),
    corr_md_1,
    corr_container,
    tsne_container,
])

content_div = html.Div([
    intro_items, html.Hr(),
    topic_charts, html.Hr(),
    sentiment_charts, html.Hr(),
    words_charts, html.Hr(),
    meta_charts, html.Hr(),
    corr_sne_charts, html.Hr(),

    html.H1(children='Examplary / static analysis'),
    examples_md_1,
    examples_div,
    about_md_1,

], id='page-content', style=CONTENT_STYLE)

app.layout = html.Div([sidebar, content_div])

# app.run(debug=True)
if __name__ == '__main__':
    app.run_server(debug=False)