"""
Import dataframe, define lists of columns / available artist, genres
etc to be used in visualizations and dash options
"""

import pandas as pd

# general df with counts of metadata, topics, POS, emotions etc
counts_df = pd.read_csv('../data/combined_count.csv', index_col=0)

# dfs with top 20 words by artist and genre, with
# stopwords and some popular words filtered out
top_20_filtered_words_genre_df = pd.read_csv('../data/top_20_filtered_words_by_genre.csv')
top_20_filtered_words_artist_df = pd.read_csv('../data/top_20_filtered_words_by_artist.csv')

# dfs with ngram counts
artist_ngrams_df = pd.read_csv('../data/artist_ngrams.csv', index_col=0)
genre_ngrams_df = pd.read_csv('../data/genre_ngrams.csv', index_col=0)

# mean and sum group stats by genre
genre_mean_df = pd.read_csv('../data/genre_mean_df.csv', index_col = 0)
genre_sum_df = pd.read_csv('../data/genre_sum_df.csv', index_col = 0)

# mean and sum group stats by artist
artist_mean_df = pd.read_csv('../data/combined_artists_mean.csv', index_col = 0)
artist_sum_df = pd.read_csv('../data/combined_artists_sum.csv', index_col = 0)

# frequency counts vs other for genre and artists
artist_freq_dist_df = pd.read_csv('../data/freq_dist_comparisons_raw.csv', index_col=0)
genre_freq_dist_df = pd.read_csv('../data/genre_freq_dist_comparisons_raw.csv', index_col=0)

# sentiments for artist and genres
genre_sentiment_counts_df = pd.read_csv('../data/genre_sentiment_counts.csv', index_col = 0)
artist_sentiment_counts_df = pd.read_csv('../data/artist_sentiment_counts.csv', index_col = 0)


# options
artists = list(counts_df.Artist.unique())
genres = list(counts_df.genre.unique())

topics = [
 'manual_love_count',
 'manual_money_count',
 'manual_violence_count',
 'manual_drugs_count',
 'manual_gendered_count',
 'manual_sadness_count',
 'manual_joy_count',
 'manual_yes_count',
 'manual_no_count'
]

# for metadata graphs
meta_columns = ['unique_words', 'total_words',
                'featured_count', 'producer_count',
                'writer_count']


# for wordclouds
# column access names
count_cols = []
word_cols = []
n = 20
for ind in range(n):
    word_cols.append(f'word{ind}')
    count_cols.append(f'word{ind}_count')

# artists with genre and gender
artist_df = pd.read_csv('../data/artist_df.csv', index_col=0)

# embeddings
tsne_df = pd.read_csv('../data/artist_lyrics_embeddings.csv')


# songs with highest topic counts
topic_max_df = pd.read_csv('../data/topic_max_df.csv', index_col=0)


# ---------------------------------------------------------------------------- #
#                           rap decades analysis                               #
# ---------------------------------------------------------------------------- #

decade_counts_df = pd.read_csv('../data/decade_dataframes/decades_counts.csv', index_col=0)
decade_sum_df = pd.read_csv('../data/decade_dataframes/decade_groupby_sum.csv',index_col=0)
decade_mean_df = pd.read_csv('../data/decade_dataframes/decade_groupby_mean.csv',index_col=0)
decade_artist_sum_df = pd.read_csv('../data/decade_dataframes/artist_groupby_sum.csv',index_col=0)
decade_artist_mean_df = pd.read_csv('../data/decade_dataframes/artist_groupby_mean.csv',index_col=0)
top_20_words_by_decade_df = pd.read_csv(
    '../data/decade_dataframes/top_20_filtered_words_by_decade.csv' ,index_col=0)

decade_topics = [ 'manual_love_count',
                 'manual_swears_count',
                 'manual_money_count',
                 'manual_violence_count',
                 'manual_drugs_count',
                 'manual_gendered_count',
                 'manual_sadness_count',
                 'manual_joy_count',
                 'manual_yes_count',
                 'manual_no_count' ]

top_20_words_by_decade_df['decade'] = top_20_words_by_decade_df.index