from dash import Dash, html, dcc, callback, Output, Input, dash_table
import dash_bootstrap_components as dbc

from dataframes import (
    counts_df, artist_df
)
# ---------------------------------------------------------------------------- #
#                                markdown intro                                #
# ---------------------------------------------------------------------------- #
md_intro_1 = dcc.Markdown(
'''
    Analyzing relationships between lyrics content of selected artists from selected genres.  
    The genres are: pop, rap, rock and soul  
    And artists include:  
'''
,id='md-intro'
)

md_intro_2 = dcc.Markdown(
'''
    The lyrics representing each artists were collected from [genius.com](https://genius.com)
    using an API wrapper by [John W. Miller](https://github.com/johnwmillr/LyricsGenius), whose
    [post](https://www.johnwmillr.com/trucks-and-beer/) also partially inspired the project.

    The main metric of artist choice was personal taste, but was also guided by popularity of
    artist releases as seen on [rateyourmusic.com](https://rateyourmusic.com/), whereas the songs
    were the first 20 songs of their available lyrics discography, sorted by popularity on Genius,
    whilst skipping songs that were remixes, intrumentals, live versions or had no lyrics in general.
    
    With 20 songs per artist and 10 artist per genre (for a total of 800 songs),
    the analysis can at best be considered shallow or as an attempt of estimating population (genre)
    relations from a small sample.  
    Nevertheless the topic is interesting, an the results may intrigue.

    Below a referential table with gathered artist data can be seen, where key columns with non-obvious names include:
    * featured / producer / writer_count - extra metadata for each song about - the number of artists featured
    on the song and the song producer and writer credit counts
    * unique / total_words - the counts of unique and total words used in each song
    * manual_..._count - the count of references to topics / word groups - explained later
    * CC/CD/... - part of speech counts
'''
)

md_intro_3 = dcc.Markdown(
'''
    The main areas of analysis include:
    * Comparing topic mentions / themes between artist and genre lyrical corpuses
    * Comparing sentiments and emotions
    * Comparing words used across genres, words unique to artists, getting deeper
    * Using song and artist metadata
    * Looking at correlations / groupings

    The main portion of this project is the interactive part, where the user can choose which metrics,
    for which artists and genres they want to generate the charts, but a static analysis / exploration
    was also provided, along with additional information about the data gathering, exploration, engineering
    and general creation process.
'''
)

# ---------------------------------------------------------------------------- #
#                       df table and extra markdown intro                      #
# ---------------------------------------------------------------------------- #

## table
counts_df_table = dash_table.DataTable(
    counts_df.to_dict('records'),
    columns=[{"name": c, "id": c} for c in counts_df.columns],

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
    id='counts-df'
)
## table
artist_df_table = dash_table.DataTable(
    artist_df.to_dict('records'),
    columns=[{"name": c, "id": c} for c in artist_df.columns],

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
    id='artist-df'
)

