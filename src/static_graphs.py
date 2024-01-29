from dash import Dash, html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc

import plotly.io as pio
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as graph_objects

from wordcloud import WordCloud

from dataframes import (
    counts_df,
    artist_mean_df,
    genre_sentiment_counts_df, artist_sentiment_counts_df,
    top_20_filtered_words_genre_df, top_20_filtered_words_artist_df,
    meta_columns, topics, genres, artists,
    word_cols, count_cols,
    tsne_df
)

# ---------------------------------------------------------------------------- #
#                              correlation matrix                              #
# ---------------------------------------------------------------------------- #

to_corr = ['Year', 'Month', 'Day', 'Pageviews', *meta_columns, *topics]
pio.templates.default = "plotly_white"

corr = counts_df[to_corr].corr()

corr_map = graph_objects.Heatmap(
    z = corr,
    x=corr.columns,
    y=corr.columns,
    colorscale=px.colors.diverging.RdBu,
    zmin=-1,
    zmax=1
)

corr_fig = graph_objects.Figure()
corr_fig.add_trace(corr_map)


corr_container = dbc.Container([
    html.H3(children = 'Correlation Matrix', style={'textAlign': 'center'}),
    dcc.Graph(id='corr-graph-content',
             figure = corr_fig)
], fluid=True)


# ---------------------------------------------------------------------------- #
#                 spine graph for topics for female/male split                 #
# ---------------------------------------------------------------------------- #

#artist_mean_df
topic_cols = [col for col in list(artist_mean_df.columns) if col.endswith('percent')]
topic_cols_no_gendered = [col for col in topic_cols if not 'gendered' in col]

gender_grouped = artist_mean_df[['gender', *topic_cols]].groupby(['gender']).mean()
female_row = gender_grouped.loc['female', :]
female_row = female_row * -1

male_row = gender_grouped.loc['male', :]

topic_spine_fig = graph_objects.Figure(
    data = [
        graph_objects.Bar(name='male',
                          y = topic_cols_no_gendered,
                          x = male_row.tolist(),
                          orientation='h',
                          marker=dict(color='#DD5555',
                                     line=dict(
                                     color='rgba(0,0,0,1.0)', width=0.5)),
                          hoverinfo='none'
                         ),
        graph_objects.Bar(name='female',
                  y = topic_cols_no_gendered,
                  x = female_row.tolist(),
                  orientation='h',
                  marker=dict(color='#5555DD',
                             line=dict(
                             color='rgba(0,0,0,1.0)', width=0.5)),
                  hoverinfo='none'
                 ),
        
    ],
)
topic_spine_fig.update_layout(barmode='relative')

topic_spine_container = dbc.Container([
    html.H3(children = 'Topic mentions comparison between male and female artist', style={'textAlign': 'center'}),
    dcc.Graph(id='topic-spine-graph-content',
             figure = topic_spine_fig)
], fluid=True)



# ---------------------------------------------------------------------------- #
#       static spine graph for positive / negative genre and artist split      #
# ---------------------------------------------------------------------------- #
genre_positives = list(genre_sentiment_counts_df['positive'])
genre_negatives = list(genre_sentiment_counts_df['negative'])
genre_negatives = [-1 * neg for neg in genre_negatives]
genre_neutrals_negative = [-1 * neutral/2 for neutral in genre_sentiment_counts_df['neutral']]
genre_neutrals_positive = [neutral/2 for neutral in genre_sentiment_counts_df['neutral']]

genre_sentiment_spine_fig = graph_objects.Figure(
    data = [
        graph_objects.Bar(name='Neutral',
                          y=genres,
                          x = genre_neutrals_positive,
                          orientation='h',
                          marker=dict(color='#DDDD55',
                                     line=dict(
                                     color='rgba(0,0,0,1.0)', width=0.5)),
                          hoverinfo='none'
                         ),
        graph_objects.Bar(showlegend=False,
                          y=genres,
                          x = genre_neutrals_negative,
                          orientation='h',
                          marker=dict(color='#DDDD55',
                                     line=dict(
                                     color='rgba(0,0,0,1.0)', width=0.5)),
                          hoverinfo='none'
                         ),
        graph_objects.Bar(name='Positive',
                          y=genres,
                          x = genre_positives,
                          orientation='h',
                          marker=dict(color='#DD5555',
                                     line=dict(
                                     color='rgba(0,0,0,1.0)', width=0.5)),
                          hoverinfo='none'
                         ),
        graph_objects.Bar(name='Negative',
                  y=genres,
                  x = genre_negatives,
                  orientation='h',
                  marker=dict(color='#5555DD',
                             line=dict(
                             color='rgba(0,0,0,1.0)', width=0.5)),
                  hoverinfo='none'
                 ),
        
    ],
)
genre_sentiment_spine_fig.update_layout(barmode='relative')

genre_sentiment_spine_container = dbc.Container([
    html.H3(children = 'Sentiment split between genres', style={'textAlign': 'center'}),
    dcc.Graph(id='genre-sentiment-spine-graph-content',
             figure = genre_sentiment_spine_fig)
], fluid=True)


# ---------------------------------------------------------------------------- #
#                            artist sentiment spine                            #
# ---------------------------------------------------------------------------- #
artist_positives = list(artist_sentiment_counts_df['positive'])
artist_negatives = list(artist_sentiment_counts_df['negative'])
artist_negatives = [-1 * neg for neg in artist_negatives]
artist_neutrals_negative = [-1 * neutral/2 for neutral in artist_sentiment_counts_df['neutral']]
artist_neutrals_positive = [neutral/2 for neutral in artist_sentiment_counts_df['neutral']]

artist_sentiment_spine_fig = graph_objects.Figure(
    data = [
        graph_objects.Bar(name='Neutral',
                          y=artists,
                          x = artist_neutrals_positive,
                          orientation='h',
                          marker=dict(color='#DDDD55',
                                     line=dict(
                                     color='rgba(0,0,0,1.0)', width=0.5)),
                          hoverinfo='none'
                         ),
        graph_objects.Bar(showlegend=False,
                          y=artists,
                          x = artist_neutrals_negative,
                          orientation='h',
                          marker=dict(color='#DDDD55',
                                     line=dict(
                                     color='rgba(0,0,0,1.0)', width=0.5)),
                          hoverinfo='none'
                         ),
        graph_objects.Bar(name='Positive',
                          y=artists,
                          x = artist_positives,
                          orientation='h',
                          marker=dict(color='#DD5555',
                                     line=dict(
                                     color='rgba(0,0,0,1.0)', width=0.5)),
                          hoverinfo='none'
                         ),
        graph_objects.Bar(name='Negative',
                  y=artists,
                  x = artist_negatives,
                  orientation='h',
                  marker=dict(color='#5555DD',
                             line=dict(
                             color='rgba(0,0,0,1.0)', width=0.5)),
                  hoverinfo='none'
                 ),
        
    ],
)
artist_sentiment_spine_fig.update_layout(barmode='relative')

artist_sentiment_spine_container = dbc.Container([
    html.H3(children = 'Artist sentiment split', style={'textAlign': 'center'}),
    dcc.Graph(id='artist-sentiment-spine-graph-content',
             figure = artist_sentiment_spine_fig)
], fluid=True)


# ---------------------------------------------------------------------------- #
#                          genre emotion spine static                          #
# ---------------------------------------------------------------------------- #
emotions = ['sadness', 'anger', 'joy', 'fear', 'love', 'surprise']
colors = ['#5555DD', '#DD5555', '#DDDD55', '#55DD55', '#FF55DD', '#EEAA55']

genre_emotion_fig = graph_objects.Figure()

for index, emotion in enumerate(emotions):
    genre_emotion_fig.add_trace(graph_objects.Bar(
        y = genres,
        x = genre_sentiment_counts_df[emotion],
        name = emotion,
        orientation = 'h',
        marker = dict(
            color = colors[index],
            line = dict(color = colors[index], width=1)
        )
    ))
genre_emotion_fig.update_layout(barmode='stack')

genre_emotion_spine_container = dbc.Container([
    html.H3(children = 'Emotional split for genres', style={'textAlign': 'center'}),
    dcc.Graph(id='genre-emotion-spine-graph-content',
             figure = genre_emotion_fig)
], fluid=True)


# ---------------------------------------------------------------------------- #
#                         static genre wordclouds graph                        #
# ---------------------------------------------------------------------------- #

top_20_filtered_words_genre_df.rename(columns={'Unnamed: 0' : 'genre'}, inplace=True)
genres = top_20_filtered_words_genre_df['genre'].unique()

genre_wordclouds = []
genre_bars = []

for genre in genres:
    genre_df = top_20_filtered_words_genre_df[top_20_filtered_words_genre_df['genre'] == genre]
    genre_words = [genre_df[word].values[0] for word in word_cols]
    genre_counts = [genre_df[count].values[0] for count in count_cols]

    genre_item = {
        'genre': genre,
        'words': genre_words,
        'counts': genre_counts
    }

    genre_bars.append(genre_item)
    
    d = {}
    for word, count in zip(genre_words, genre_counts):
        d[word] = count

    wordcloud = WordCloud(background_color = "white", width=800, height=400)
    wordcloud.generate_from_frequencies(frequencies=d)
    genre_wordclouds.append(wordcloud)

# subplot wordcloud graph titles
genre_titles = ['pop', 'pop', 'rock', 'rock', 'rap', 'rap', 'soul', 'soul']

genre_wordclouds_fig = make_subplots(rows=4, cols=2, subplot_titles = genre_titles)

for i, genre in enumerate(genres):
    genre_wordclouds_fig.add_trace(graph_objects.Image(z=genre_wordclouds[i]), row = i+1, col = 1)
    genre_wordclouds_fig.add_trace(graph_objects.Bar(x=genre_bars[i]['words'], y=genre_bars[i]['counts'], showlegend = False), row=i+1, col=2,)
genre_wordclouds_fig.update_layout(height = 4 * 400)

# ======= container ========
genre_wordcloud_container = dbc.Container([
    html.H3(children = 'Top 20 (filtered) words by genre WordCloud', style={'textAlign': 'center'}),
    dcc.Graph(id='genre-wordcloud-graph-content',
             figure = genre_wordclouds_fig)
], fluid=True)

sentiment_md_1 = dcc.Markdown(
'''
    Having considered topical mentions, some relations can become to form. Exploring that further,
    a machine learning-based approach was taken to determine the general sentiment (positive, negative, neutral)
    and the general emotion conveyed by each song.

    For sentiment analysis, a pretrained VADER (Valence Aware Dictionary and sEntiment Reasoner) analyzer
    was used from the popular language processing library [NTLK](https://www.nltk.org/),
    which's accuracy may not be perfect, as it was intended to be used for more short-form texts,
    but it may provide a good guiding point.

    Also necessary to mention, not only are lyrics text usually longer form, but often include repetitions,
    for choruses and otherwise, which may guide models, but also, a key component of lyricsm are 
    aristic tools such as abstractions, implication and entendres, leaving the songs to more open,
    non-direct interpretation.

    For emotional classification, a pre-trained [model](https://huggingface.co/mrm8488/t5-base-finetuned-emotion), which
    was itself transfer-trained from google's T5 text-to-text model
'''
)


tsne_fig = px.scatter(tsne_df, x='x', y='y', color='genre', hover_data=['Artist'])

tsne_container = dbc.Container([
    html.H3(children = 't-SNE artist lyrics embeddings relations', style={'textAlign': 'center'}),
    dcc.Graph(id='tsne-graph-content',
             figure = tsne_fig)
], fluid=True)

corr_md_1 = dcc.Markdown(
'''
    Finally, potential correlations between various available metrics were explored with
    a correlation matrix and an attempt at visualizing relations between artists and genres by their lyrics,
    achieved through firstly vectorizing the combined lyrics for each artist into vectors of large size using a pretrained
    BERT-based Doc2Vec [model](https://www.analyticsvidhya.com/blog/2020/08/top-4-sentence-embedding-techniques-using-python/)
    , then using scikit-learn's t-SNE implementation of a dimensionality reduction transformation, for visualization purposes

    Because of t-SNE's approximal behaviour and heavy dimensionality reduction, the results are to be taken with apprehension,
    certain correlations can nevertheless be seen between genres and artists within them.
'''
)