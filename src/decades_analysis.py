from dash import Dash, html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc

import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as graph_objects

from wordcloud import WordCloud

from dataframes import (
    decade_counts_df,
    decade_sum_df,
    decade_mean_df,
    decade_artist_sum_df,
    decade_artist_mean_df,
    top_20_words_by_decade_df,
    decade_topics
)

# ---------------------------------------------------------------------------- #
#                            Topic counts by decade                            #
# ---------------------------------------------------------------------------- #

decade_bar_topic_controls = dbc.Card(
    [
        html.Div(
            [
            dbc.Label("Manual word topic"),
            dcc.Dropdown(options = decade_topics,
                        value = ['manual_love_count',],
                        id='decade-bar-topic-selection',
                        multi=True)
            ]),
    ],
    body=True,
)

decade_bar_topic_container = dbc.Container([
    html.H3(children = 'Topic mentions by decade for rap', style={'textAlign': 'center'}),
    dbc.Row(
        [
            dbc.Col(decade_bar_topic_controls, md=4),
            dbc.Col(dcc.Graph(id='decade-bar-topic-graph-content'), md=8),
        ],
        align="center",
    ),
], fluid=True)

def get_decade_bar_topic_callbacks(app):
    @app.callback(
        [
            Output('decade-bar-topic-graph-content', 'figure'),
        ],
        [
            Input('decade-bar-topic-selection', 'value'),
        ]
    )
    def update_decade_bar_topic_graph(topics):
        bar_fig = graph_objects.Figure()
        # in case there is only one selected topic - turn input into a list:
        topics_list = [topic for topic in topics]
        for topic in topics_list:
            bar_fig.add_trace(graph_objects.Bar(y=decade_sum_df[topic].values,
                                                x=decade_sum_df.index, name=topic))
        
        # return bar_fig, f'topics: {topics} topics_list: {topics_list}'
        return [bar_fig,]

# ---------------------------------------------------------------------------- #
#        Histogram for genre and chosen metric and chosen number of bins       #
# ---------------------------------------------------------------------------- #

decade_hist_topic_controls = dbc.Card(
    [
        html.Div(
            [
            dbc.Label("Metadata metric"),
            dcc.Dropdown(options = decade_topics,
                        value = ['manual_love_count',],
                        id='decade-hist-topic-selection',
                        multi=True)
            ]),
        html.Div(
            [
            dbc.Label("Genre"),
            dcc.Dropdown(options = list(decade_counts_df['decade'].unique()),
                        value = ['2000s',],
                        id='decade-hist-decade-selection')
            ]),
        html.Div([
            dbc.Label("Number of bins"),
            dcc.Slider(1, 20, 1,
                       value = 10,            
                        id = 'decade-hist-bins-selection'
                       ),
            ])
    ],
    body=True,
)

decade_hist_topic_container = dbc.Container([
    html.H3(children = 'Topical mentions distribution by decade (counts)',
             style={'textAlign': 'center'}),
    dbc.Row(
        [
            dbc.Col(decade_hist_topic_controls, md=4),
            dbc.Col(dcc.Graph(id='decade-hist-topic-graph-content'), md=8),
        ],
        align="center",
    ),
], fluid=True)

def get_decade_hist_topic_callbacks(app):
    @app.callback(
        [
            Output('decade-hist-topic-graph-content', 'figure'),
        ],
        [
            Input('decade-hist-topic-selection', 'value'),
            Input('decade-hist-decade-selection', 'value'),
            Input('decade-hist-bins-selection', 'value'), 
        ]
    )
    def update_decade_hist_topic_graph(topic, decade, nbins):
        decade_df = decade_counts_df[decade_counts_df['decade'] == decade]
        hist_fig = px.histogram(decade_df, x=topic, nbins=nbins)
        return [hist_fig,]

# ---------------------------------------------------------------------------- #
#      Artist metadata (unique_words, producer_count etc) means by decade      #
# ---------------------------------------------------------------------------- #

meta_columns = ['unique_words', 'total_words', 'featured_count',
                'producer_count', 'writer_count']

#decade_mean_df
decade_metadata_controls = dbc.Card(
    [
        html.Div(
            [
            dbc.Label("Metadata selection"),
            dcc.Dropdown(options = meta_columns,
                        value = 'unique_words',
                        id='decade-metadata-selection')
            ]),
    ],
    body=True,
)

decade_metadata_container = dbc.Container([
    html.H3(children = 'Artist metadata mean by decade comparison', style={'textAlign': 'center'}),
    dbc.Row(
        [
            dbc.Col(decade_metadata_controls, md=4),
            dbc.Col(dcc.Graph(id='decade-metadata-graph-content'), md=8),
        ],
        align="center",
    ),
], fluid=True)

def get_decade_medatata_callbacks(app):
    @app.callback(
        [
            Output('decade-metadata-graph-content', 'figure'),
        ],
        [
            Input('decade-metadata-selection', 'value'),
        ]
    )
    def update_decade_metadata_graph(meta_col):
        meta_fig = px.bar(decade_mean_df, x=decade_mean_df.index, y=decade_mean_df[meta_col])
        return [meta_fig,]
    

# ---------------------------------------------------------------------------- #
#                      Artist metadata by artist (decades)                     #
# ---------------------------------------------------------------------------- #

# decade_artist_mean_df
decade_artist_metadata_controls = dbc.Card(
    [
        html.Div(
            [
            dbc.Label("Metadata selection"),
            dcc.Dropdown(options = meta_columns,
                        value = 'unique_words',
                        id='decade-artist-metadata-selection')
            ]),
    ],
    body=True,
)

decade_artist_metadata_container = dbc.Container([
    html.H3(children = 'Artist metadata mean by artist comparison', style={'textAlign': 'center'}),
    html.P(id="decade-artist-metadata-df-shape"),
    dbc.Row(
        [
            dbc.Col(decade_artist_metadata_controls, md=4),
            dbc.Col(dcc.Graph(id='decade-artist-metadata-graph-content'), md=8),
        ],
        align="center",
    ),
], fluid=True)

def get_decade_artist_metadata_callbacks(app):
    @app.callback(
        [
            Output('decade-artist-metadata-graph-content', 'figure'),
        ],
        [
            Input('decade-artist-metadata-selection', 'value'),
        ]
    )
    def update_decade_artist_metadata_graph(meta_col):
        meta_fig = px.bar(decade_artist_mean_df, x=decade_artist_mean_df['Artist'],
                        y=decade_artist_mean_df[meta_col])
        return [meta_fig,]
    

# ---------------------------------------------------------------------------- #
#                       static correlation matrix decades                      #
# ---------------------------------------------------------------------------- #
import plotly.io as pio

to_corr = ['Year', 'Month', 'Day', 'Pageviews', *meta_columns, *decade_topics]
pio.templates.default = "plotly_white"

decade_corr = decade_counts_df[to_corr].corr()

decade_corr_map = graph_objects.Heatmap(
    z = decade_corr,
    x=decade_corr.columns,
    y=decade_corr.columns,
    colorscale=px.colors.diverging.RdBu,
    zmin=-1,
    zmax=1,
)

decade_corr_fig = graph_objects.Figure()
decade_corr_fig.add_trace(decade_corr_map)
# fig.show()

decade_corr_container = dbc.Container([
    html.H3(children = 'Decade correlation matrix', style={'textAlign': 'center'}),
    dcc.Graph(id='decade-corr-graph-content',
             figure = decade_corr_fig)
], fluid=True)


# ---------------------------------------------------------------------------- #
#                       top 20 words by decade wordclouds                      #
# ---------------------------------------------------------------------------- #

# setup
decades = top_20_words_by_decade_df['decade'].unique()

# column access names
count_cols = []
word_cols = []
n = 20
for ind in range(n):
    word_cols.append(f'word{ind}')
    count_cols.append(f'word{ind}_count')

decade_wordclouds = []
decade_bars = []

for decade in decades:
    decade_df = top_20_words_by_decade_df[top_20_words_by_decade_df['decade'] == decade]
    decade_words = [decade_df[word].values[0] for word in word_cols]
    decade_counts = [decade_df[count].values[0] for count in count_cols]

    decade_item = {
        'decade': decade,
        'words': decade_words,
        'counts': decade_counts
    }

    decade_bars.append(decade_item)
    
    d = {}
    for word, count in zip(decade_words, decade_counts):
        d[word] = count

    wordcloud = WordCloud(background_color = "white", width=800, height=400)
    wordcloud.generate_from_frequencies(frequencies=d)
    decade_wordclouds.append(wordcloud)

decade_titles = ['1980s', '1980s', '1990s', '1990s', '2000s', '2000s', '2010s', '2010s', '2020s', '2020s']

decade_wordclouds_fig = make_subplots(rows=5, cols=2, subplot_titles = decade_titles)

for i, decade in enumerate(decades):
    decade_wordclouds_fig.add_trace(graph_objects.Image(z=decade_wordclouds[i]), row = i+1, col = 1)
    decade_wordclouds_fig.add_trace(graph_objects.Bar(x=decade_bars[i]['words'], y=decade_bars[i]['counts'],
                                                      showlegend = False), row=i+1, col=2,)
decade_wordclouds_fig.update_layout(height = 5 * 400)

decade_wordcloud_container = dbc.Container([
    html.H3(children = 'Top 20 (filtered) words by decade wordclouds', style={'textAlign': 'center'}),
    dcc.Graph(id='decade-wordcloud-graph-content',
             figure = decade_wordclouds_fig)
], fluid=True)

decades_md_1 = dcc.Markdown(
'''
    As a supplement / a further example of using the created data engineering tools for comparins lyrical contents,
    an analysis of of rap artists lyrics between decades is presented,
    where the affiliation with a decade was chosen semi-manually, partially by the popularity
    rankings of artist releases on [rateyourmusic](https://rateyourmusic.com/), even though some of
    the artists considered have been in the scene for multiple decades.

    The decades considered include the 1980s, 1990s, 2000s, 2010s, 2020s, each one represented by 10 artists,
    20 songs from each artist (again chosen as the 20 most popular artist songs on genius.com), for
    a total dataset size of 1000 songs, split across 5 decades.
'''    
)

decades_md_2 = dcc.Markdown(
'''
    At a quick glance, some potential relationships between the decades can be seen,
    although possibly guided by artist choice and not definitive to the population.

    For example:  
    * Looking at the change in total and unique word count means across decades, a reduction
    in vocabulary size can be noticed, while the number of total words seemingly doesn't change much,
    possibly implying a higher reliance on repetition (hooks, choruses) in newer songs
    * As time went on, mentions of love-related words seem to have been overtaken by money-related ones.
    Has hip-hop lost its tender side and replaced it wish cold cash?
    * Albeit with some slight changes, the top words to seem to have stayed the same as time went on
'''
)

decades_images_1 = html.Div([
    html.P(children='Unique words mean by decade', style={'textAlign': 'center'}),
    html.Img(src='assets/decades_total_words.png'),
    html.P(children='Total words mean by decade', style={'textAlign': 'center'}),
    html.Img(src='assets/decades_unique_words.png'),
    html.P(children='Decades love vs money', style={'textAlign': 'center'}),
    html.Img(src='assets/decades_topic_love_money.png'),
])

