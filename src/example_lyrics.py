# Find specific lyrics which have the most topical word mentions

import pandas as pd

from dash import Dash, html, dcc, callback, Output, Input, dash_table
import dash_bootstrap_components as dbc

from dataframes import (
    counts_df, topics
)

# columns of interest
topic_max_cols = ['Artist', 'Song Title', 'Song Lyrics', 'genre', 'gender']

topic_max_df = pd.DataFrame(columns=[*topic_max_cols, 'topic'])

for topic in topics:
    topic_max = counts_df[topic].max()
    topic_max_row = counts_df[counts_df[topic] == topic_max]
    # topic_max_row_df = pd.DataFrame([topic_max_row])
    
    topic_max_row = topic_max_row[[*topic_max_cols]]
    topic_max_row['topic'] = topic
    
    topic_max_df = pd.concat([topic_max_df, topic_max_row], axis=0)

topic_max_df.reset_index(drop=True, inplace=True)

# print(topic_max_df)

# topic_max_df.to_csv('../data/topic_max_df.csv')

topic_max_md_1 = dcc.Markdown(
'''
    For futher insight, below presented are the songs that got the highest amount of each topic mentions
'''
)

topic_max_df_table = dash_table.DataTable(
    counts_df.to_dict('records'),
    columns=[{"name": c, "id": c} for c in topic_max_df.columns],

    filter_action="native",
    sort_action="native",
    # sort_mode="multi",

    page_action="native",
    page_current= 0,
    page_size= 10,
    style_cell={'textAlign': 'left'},

    style_as_list_view=True,
    style_data={
        'color': 'black',
        'backgroundColor': 'white'
    },
    style_data_conditional=[
        {
            'if': {'row_index': 'odd'},
            'backgroundColor': 'rgb(220, 220, 220)',
        }
    ],
    style_header={
        'backgroundColor': 'rgb(210, 210, 210)',
        'color': 'black',
        'fontWeight': 'bold'
    },
    style_table={"overflowX": "auto"},
    id='topic-max-df'
)
