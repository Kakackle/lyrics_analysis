from dash import Dash, html, dcc, callback, Output, Input
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
#                                    layout                                    #
# ---------------------------------------------------------------------------- #

app.layout = dbc.Container([
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

], fluid=True)

# app.run(debug=True)
if __name__ == '__main__':
    app.run_server(debug=False)