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
    word_cols, count_cols
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
    html.H1(children = 'Correlation matrix', style={'textAlign': 'center'}),
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
    html.H1(children = 'spine graph for topics for female/male split', style={'textAlign': 'center'}),
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
    html.H1(children = 'spine graph for genre sentiment splits', style={'textAlign': 'center'}),
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
    html.H1(children = 'spine graph for artist sentiment splits', style={'textAlign': 'center'}),
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
    html.H1(children = 'spine graph for genre emotion splits', style={'textAlign': 'center'}),
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
    html.H1(children = 'Top 20 (filtered) words by genre wordclouds', style={'textAlign': 'center'}),
    dcc.Graph(id='genre-wordcloud-graph-content',
             figure = genre_wordclouds_fig)
], fluid=True)