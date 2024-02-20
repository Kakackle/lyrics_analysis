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
    ### What is it?
    An explaratory analysis of the lyrical content of selected artists' music from 4 selected genres.
    Additionally for one of the genres (rap), a complementary analysis of changes through multiple decades was done.
    
    ### Why was it made?
    As an [avid](https://rateyourmusic.com/~Kakackle) music listener of multiple genres (and an aspiring music maker), from most corners of the world,
    I often find myself focused mostly on the rhythm, melody and harmony, leaving out the lyrics, instead making my judgments on these 3 factors.
    For this project I wanted to explore, whether significant differences, or perhaps any unique correlations, could be found
    within and between 4 of my favourite genres: **pop**, **rap**, **rock** and **soul**
    
    With curiosity and a desire to develop my data engineering skills as the main motivators, various limitations and assumptions were taken,
    particularly with regards to the artist choice and feature engineering directions, explained later.

    ### What's included?
    With the main goal being exploration, a system of interactive chart-making tools was prepared (using Python, Plotly and Dash), allowing for quick
    hypothesis testing and as an engaging data presentation tool, thererfore in this project you can find:
    * A static analysis of various relations found within and between genres
    * A robust section of interactive charts, for the user to play with, with the option of saving your charts locally
    * Static and interactive analysis of rap lyrics through decades
    * ML-based prediction of song genre from lyrical information and predicting the count of unique words per song, for artist within genre

    The artists whose lyrics were used are:  
'''
,id='md-intro'
)

md_intro_2 = dcc.Markdown(
'''
    ### How was it done?
    The lyrics representing each artists were collected from [genius.com](https://genius.com)
    using an API wrapper by [John W. Miller](https://github.com/johnwmillr/LyricsGenius), whose
    [post](https://www.johnwmillr.com/trucks-and-beer/) also partially inspired the project.

    The main metric of artist choice was personal taste, but it was also guided by the popularity of
    artist releases as seen on a music release-rating website [rateyourmusic.com](https://rateyourmusic.com/),
    whereas the songs themselves were the first 20 songs of each artists' available lyrics discography,
    sorted by popularity on Genius, whilst skipping songs that were remixes,
    intrumentals, live versions or had no lyrics at all, to ensure dataset purity.
    
    With 20 songs per artist and 10 artists per genre, for a total of 800 songs considered,
    the analysis can at best be considered quite limited or as an attempt of estimating population (genre)
    relations from a small sample.

    Below a referential table with gathered artist data can be seen, where key columns with non-obvious names include:
    * featured / producer / writer_count - extra metadata for each song regarsding the number of artists featured
    on the song and how many producers and writers were credited
    * unique / total_words - the counts of unique and total words used in each song
    * manual_..._count - the count of references to particular topics / word groups - explained in-depth later
    * CC/CD/... - part of speech tag counts
'''
)

md_intro_3 = dcc.Markdown(
'''
    ### The main areas of analysis include:
    * The comparison of topic mentions / thematical contents between artist and genre lyrical corpuses
    * The comparison of sentiments and emotions presented in the lyrics
    * The comparison of words used across genres, words unique to artists, low-lever differences
    * Analysis of song and artist-related metadata
    * Correlations / grouping analysis

    The main portion of this project is the interactive part, where the user can choose which metrics,
    for which artists and genres they want to generate the charts with the a static analysis / exploration of
    some of the metrics provided, along with additional information about the data gathering, exploration, engineering
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

