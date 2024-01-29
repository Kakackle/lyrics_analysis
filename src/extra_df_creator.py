import pandas as pd

from dataframes import (
    counts_df
)

# print(counts_df.columns)

# print(counts_df.head())

artist_df = counts_df[['genre', 'Artist', 'gender']].drop_duplicates().reset_index(drop=True)

artist_df.to_csv('../data/artist_df.csv')

artist_df_grouped = artist_df.groupby(by=['genre',])

print(artist_df_grouped.head())