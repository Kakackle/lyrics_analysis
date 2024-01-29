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
    html.H3(children = 'Words more common to one artist than others',
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
    html.H3(children = 'Words more are common to one genre than others',
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
    
freq_md_1 = dcc.Markdown(
'''
    For this part of analysis, a deeper look at of what words do the analyzed lyrcic actually comprise
    and can we find any noticable relations between artists, genres etc. For example are there particular
    words of phrases that often get used within a genre or between genres.
    
    For this, using [TextBlob](https://textblob.readthedocs.io/en/dev/) - a NLTK wrapper library,
    both the frequencies of occurences of words in songs (ignoring popular english stopwords
    and some other common words such as "I", "get" etc) were taken, as well as frequencies of occurences
    of their common n-grams (word groupings, phrases) of length 2,3 and 4.

    The visualization of most frequent words for genres and artistst are presented both in a Wordcloud
    (using the [WordCloud](https://amueller.github.io/word_cloud/) library) and the bar chart forms.

    Additionally, inspired by a post from [Degenerate State](https://www.degeneratestate.org/posts/2016/Apr/20/heavy-metal-and-natural-language-processing-part-1/),
    a metric of "uniqueness" was created for words used by each artist and within each genre, which was calculated by the equation:
    $\log(occurences_in_artist / occurences_in_others)$
'''
)