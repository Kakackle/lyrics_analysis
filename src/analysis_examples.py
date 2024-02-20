from dash import Dash, html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc

import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as graph_objects

from skimage import io

# artist_bar_topic_rap_img = io.imread('../results/topic_counts_by_artist_rap_example.PNG')
# artist_bar_topic_rap_fig = px.imshow(artist_bar_topic_rap_img)

# artist_bar_topic_pop_img = io.imread('../results/topic_counts_by_artist_pop_example.PNG')
# artist_bar_topic_pop_fig = px.imshow(artist_bar_topic_pop_img)

# artist_bar_topic_examples = dbc.Container([
#     html.H3(children='Topical analysis examples', id='artist-bar-topic-examples'),

#     dbc.Row(
#             [
#                 dbc.Col(
#                     html.Div(
#                         [
#                             dcc.Graph(figure = artist_bar_topic_rap_fig),
#                             html.P(children = "Example 1 - Nas seems to be a rather sad artist in his lyrics")
#                         ]
#                     ), md=6
#                 ),
#                 dbc.Col(
#                     html.Div(
#                         [
#                             dcc.Graph(figure = artist_bar_topic_pop_fig),
#                             html.P(children = "Example 2 - Aaliyah was very much about love, not unlike her genre peers though, \
#                                    except for Olivia Rodgrigo and Taylor Swift, who tend to write about breakups")
#                         ]
#                     ), md=6
#                 )

#             ],
#             align='center'
#         ),

# ])

# examples_div = html.Div(
#     [
#         artist_bar_topic_examples,
#     ],
#     id='examples-div'
# )

examples_md_1 = dcc.Markdown(
'''
    Additionally, as stated in the introduction, static example comparisons / observations
    were taken, to provide further insight / a proper, non-interactive analysis.

    ### Topical analysis

    Observing topical mentions between genres, a strong tendecy towards love-related topics can be seen for all genres,
    but especially for pop and soul it seem to be a contributing factor.

    For ease of comparison between other topics, a second chart is shown, with 'love' counts excluded.
''',
id = 'examples-topical'
)

# img_path = 'assets/counts_by_genre_bar.png'

topic_images_1 = html.Div([
    html.P(children='Topical counts by genre', style={'textAlign': 'center'}),
    html.Img(src='assets/counts_by_genre_bar.png', alt='Topical counts by genre'),
    html.P(children='Topical counts by genre with "love" excluded', style={'textAlign': 'center'}),
    html.Img(src='assets/counts_by_genre_no_love_bar.png', alt='Topical counts by genre'),
])

# ![Topical counts by genre bar chart]('../results/counts_by_genre_bar.png')

# <p float="left" align="middle">
#     <img src="../results/counts_by_genre_bar.png" width="100" alt="topical counts bar chart"/>
#     <img src="../results/counts_by_genre_no_love_bar.png" width="100" alt="topical counts bar chart"/> 
# </p>

examples_md_2 = dcc.Markdown(
'''
    Looking at within-genre artist comparisons, for pop, some standouts when it comes to love-like topics
    include Olivia Rodrigo and Taylor Swift, which often do tend to write about breakups or otherwise unsatisfactory
    relationships.

    For rap, a slight tendency for Nas to write about sadder topics could be determined, while Kendrick and Eminem do tend
    to mention violent topics, though for different reasons - Kendrick often damning violence in his lyrics,
    Eminem claiming to engage in it.
'''
)

topic_images_2 = html.Div([
    html.P(children='Pop artists and love', style={'textAlign': 'center'}),
    html.Img(src='assets/pop_love_count_bar.png', alt='Pop artists and love'),
    html.P(children='Rap artists topically', style={'textAlign': 'center'}),
    html.Img(src='assets/rap_violence_money_sadness_bar.png', alt='Rap artists topically'),
])


examples_md_3 = dcc.Markdown(
'''
    ### Sentiment analysis

    Bearing in mind topical mention results, can similar conclusions be reached from looking at
    sentiment and emotion-based analysis? Having in mind the imperfections of models used, a strong
    tendency of pop and soul artists to mention love-related topics could guide the algorithms to grade
    the songs as positive, whilst a more varied spread of topics could be related to the higher amount of
    neutrally graded songs for rap.

    Similar conclusions could be reached for the emotional analysis, though the overwhelming majority
    of 'joy'-classified songs should perhaps warrant a deeper look at the exact data that the model was trained on.
''',
id = 'examples-sentiment'
)

sentiment_images = html.Div([
    html.P(children='Genre sentiment split', style={'textAlign': 'center'}),
    html.Img(src='assets/sentiment_split_genre.png'),
    html.P(children='Genre emotion split', style={'textAlign': 'center'}),
    html.Img(src='assets/emotion_split_genre.png'),
])

examples_md_4 = dcc.Markdown(
'''
    ### Word usage analysis

    As noted in the introduction, the amount of songs considered for each genre and each artist was quite limited.
    Such a decision was made in the initial planning of this analysis as to try to capture the essential parts of the possible differences
    between genres, artists and otherwise, without having to look at unmanageable amounts of data.
    A possible continuation of this project could perhaps include more data, validating whether the results change.

    As a result of the scale of the project, Carly Rae Jepsen's vocabulary seems to include the word 'hijack' with a quite
    high uniqueness score attached to it. This is a result of her song 'Making the Most of the Night' being included in the
    dataset, which mentions the word over 20 times, whilst other songs across other genres use this word sparingly.

    As seen later (or above, in the interactive part), when compared with an artist such as Taylor Swift,
    Carly Rae Jepsen tends to on average have a much (with a difference over 100) smaller vocabulary of unique words per song.
    This might explain, why Taylor, who generally has a high vocabulary, but doesn't necessarily make long songs, doesn't seem
    to have words significantly unique to her - word reuse seems to be much lower in her songs than Carly's.

    Looking at unique words by genre, rap lyrics seem to be uniquely violent. At least when compared to these other manually chosen genres
    and the manually chosen artists representing them.
''',
id = 'examples-words'
)

unique_word_images_1 = html.Div([
    html.P(children='Words unique for Carly Rae Jepsen', style={'textAlign': 'center'}),
    html.Img(src='assets/carly_rae_unique_word_hijack_small_dataset.png'),
    html.P(children='Words unique for Taylor Swift', style={'textAlign': 'center'}),
    html.Img(src='assets/taylor_unique_words.png'),
    html.P(children='Words unique for rap', style={'textAlign': 'center'}),
    html.Img(src='assets/rap_unique_words.png'),
])

examples_md_5 = dcc.Markdown(
'''
    Comparing the mean counts of unique words used in genres, rap can be seen as a confident winner,
    which also correlates with the mean of total words used, but also - with the mean of number of featured artists.
    Rap songs tend to be more focused on having multiple verses rather than on choruses, but a higher tendency to feature
    other artist on songs could perhaps explain this - every artist will probably have something different to say in their verse.
''',
id = 'examples-meta'
)

unique_word_images_2 = html.Div([
    html.P(children='Unique words mean by genre', style={'textAlign': 'center'}),
    html.Img(src='assets/unique_words_genres.png'),
    html.P(children='Total words mean by genre', style={'textAlign': 'center'}),
    html.Img(src='assets/total_words_genres.png'),
    html.P(children='Featured artist count mean by genre', style={'textAlign': 'center'}),
    html.Img(src='assets/featured_count_genres.png'),
])

examples_md_6 = dcc.Markdown(
'''
    ### Metadata

    Looking at metadata analysis results further, some outliers and peculiar correlations can be found.
    
    Kanye West for example, can be seen to work with a significantly higher average amount of writers - which
    is True for parts of his discography, which also tend to be his most popular songs, which perhaps incluenced the results.

    A similar, eyebrow-raising correlation can also be found between the tendency to mention sadness-related topics and the mean
    count of producers - can a work enviroment with higher amount of producers influence emotions or is this a random
    occurence stemming from the limitations of such analysis? Most likely the latter.
'''
)

meta_images = html.Div([
    html.P(children='Mean writer count by artist', style={'textAlign': 'center'}),
    html.Img(src='assets/kanye_writer_count.png'),
    html.P(children='Sadness and producers', style={'textAlign': 'center'}),
    html.Img(src='assets/sadness_producer.png'),
])