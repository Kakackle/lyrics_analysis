"""
Import dataframe, define lists of columns / available artist, genres
etc to be used in visualizations and dash options
"""

import pandas as pd

# general df with counts of metadata, topics, POS, emotions etc
counts_df = pd.read_csv('./data/combined_count.csv', index_col=0)

# dfs with top 20 words by artist and genre, with
# stopwords and some popular words filtered out
top_20_filtered_words_genre_df = pd.read_csv('./data/top_20_filtered_words_by_genre.csv')
top_20_filtered_words_artist_df = pd.read_csv('./data/top_20_filtered_words_by_artist.csv')

# dfs with ngram counts
artist_ngrams_df = pd.read_csv('./data/artist_ngrams.csv', index_col=0)
genre_ngrams_df = pd.read_csv('./data/genre_ngrams.csv', index_col=0)

# mean and sum group stats by genre
genre_mean_df = pd.read_csv('./data/genre_mean_df.csv', index_col = 0)
genre_sum_df = pd.read_csv('./data/genre_sum_df.csv', index_col = 0)

# mean and sum group stats by artist
artist_mean_df = pd.read_csv('./data/combined_artists_mean.csv', index_col = 0)
artist_sum_df = pd.read_csv('./data/combined_artists_sum.csv', index_col = 0)

# frequency counts vs other for genre and artists
artist_freq_dist_df = pd.read_csv('./data/freq_dist_comparisons_raw.csv', index_col=0)
genre_freq_dist_df = pd.read_csv('./data/genre_freq_dist_comparisons_raw.csv', index_col=0)

# sentiments for artist and genres
genre_sentiment_counts_df = pd.read_csv('./data/genre_sentiment_counts.csv', index_col = 0)
artist_sentiment_counts_df = pd.read_csv('./data/artist_sentiment_counts.csv', index_col = 0)


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