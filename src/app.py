from dash import Dash, html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

from wordcloud import WordCloud
from plotly.subplots import make_subplots
import plotly.graph_objects as graph_objects

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
    topic_scatter_container, get_topic_scatter_callbacks
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

# @app.callback(
#     [
#         Output('artist-freq-dist-graph-content', 'figure'),
#         Output('artist-freq-dist-df-shape', 'children')
#     ],
#     [
#         Input('freq-dist-artist-selection', 'value'),
#     ]
# )
# def update_artist_freq_dist_graph(artists):
#     artist_dist_fig = graph_objects.Figure()
#     for artist in artists:
#         artist_comp_dict = artist_freq_dist_df[artist_freq_dist_df['Artist'] == artist]['sorted_comparison_dict'].values[0]
#         artist_comp_dict = ast.literal_eval(artist_comp_dict)
#         artist_comp_dict_no_unique = {k: v for k,v in artist_comp_dict.items() if v != 1000}
#         no_unique_20 = take(20, artist_comp_dict_no_unique.items())
#         words = [word[0] for word in no_unique_20]
#         counts = [word[1] for word in no_unique_20]
        
#         artist_dist_fig.add_trace(graph_objects.Bar(x=words, y=counts, name=artist))
                                  
#     return artist_dist_fig, f''



# ---------------------------------------------------------------------------- #
#                                    layout                                    #
# ---------------------------------------------------------------------------- #

app.layout = dbc.Container([
    topic_container,
    html.Hr(),
    bar_topic_container,
    html.Hr(),
    artist_bar_topic_container,
    html.Hr(),
    topic_scatter_container,
    html.Hr(),

], fluid=True)

# app.run(debug=True)
if __name__ == '__main__':
    app.run_server(debug=False)